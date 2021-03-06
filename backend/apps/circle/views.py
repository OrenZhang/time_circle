import datetime

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from apps.circle.models import Category, Item
from apps.circle.serializers import (
    CategoryReadSerializer,
    CategorySerializer,
    ItemListSerializer,
    ItemSerializer,
    ItemStopSerializer,
    OverviewRequestSerializer,
    OverviewSerializer,
)
from apps.circle.utils import StatisticHandler
from constents.statistic import STATISTIC_YEAR_CONFIG
from utils.exceptions import Error404, OperationError, ParamsNotFound, PermissionDenied
from utils.tools import duration_format


class CategoryView(ModelViewSet):
    """目录"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryReadSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        parent_ids = self.queryset.filter(creator=request.user.username).values_list(
            "parent_id", flat=True
        )
        queryset = self.queryset.filter(
            ~Q(id__in=parent_ids) & Q(creator=request.user.username)
        )
        serializer = CategoryReadSerializer(queryset, many=True)
        data = list(serializer.data)
        data.sort(key=lambda x: x["full_name"])
        return Response(data)

    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response()

    @action(methods=["GET"], detail=True)
    def level(self, request, *args, **kwargs):
        parent_id = kwargs.get("pk", None)
        if parent_id is None:
            raise ParamsNotFound("父级目录ID缺失")
        queryset = self.queryset.filter(
            creator=request.user.username, parent_id=parent_id
        )
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ItemView(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """事项"""

    queryset = Item.objects.filter(archived=False)
    serializer_class = ItemSerializer

    def verify_date(self, data):
        req_serializer = OverviewRequestSerializer(data=data)
        req_serializer.is_valid(raise_exception=True)
        start_date = req_serializer.validated_data["start_date"]
        end_date = req_serializer.validated_data["end_date"]
        return start_date, end_date

    def list(self, request, *args, **kwargs):
        start_date, end_date = self.verify_date(request.GET)
        category_ids = Category.objects.filter(
            creator=request.user.username
        ).values_list("id", flat=True)
        self.queryset = Item.objects.filter(
            archived=True,
            category_id__in=category_ids,
            start_at__date__gte=start_date,
            start_at__date__lt=end_date + datetime.timedelta(days=1),
        ).order_by("-start_at")
        self.serializer_class = ItemListSerializer
        return super().list(request, *args, **kwargs)

    @action(methods=["POST"], detail=False)
    def start(self, request, *args, **kwargs):
        if Item.objects.unfinished_item(request.user.username) is not None:
            raise OperationError("请先处理未完成事项！")
        try:
            category = Category.objects.get(
                id=request.data.get("category_id", 0), creator=request.user.username
            )
        except Category.DoesNotExist:
            raise Error404()
        item = Item.objects.create(category_id=category.id)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @action(methods=["POST"], detail=True)
    def stop(self, request, *args, **kwargs):
        instance = self.get_object()
        category = Category.objects.get(id=instance.category_id)
        if category.creator != request.user.username:
            raise PermissionDenied()
        serializer = ItemStopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        end_at = serializer.validated_data["end_at"]
        start_at = serializer.validated_data["start_at"]
        desc = serializer.validated_data["desc"]
        if end_at <= start_at:
            raise OperationError("结束时间需要大于开始时间")
        instance.start_at = start_at
        instance.end_at = end_at
        instance.desc = desc
        instance.archived = True
        instance.save()
        return Response()

    @action(methods=["GET"], detail=False)
    def todo(self, request, *args, **kwargs):
        category_ids = Category.objects.filter(
            creator=request.user.username
        ).values_list("id", flat=True)
        items = Item.objects.filter(category_id__in=category_ids, archived=False)
        if not items.exists():
            return Response({"todo": False, "item": None})
        item = items.first()
        serializer = self.get_serializer(item)
        return Response({"todo": True, "item": serializer.data})


class OverviewView(GenericViewSet):
    """预览"""

    queryset = Item.objects.all()
    serializer_class = OverviewSerializer

    def verify_date(self, data):
        req_serializer = OverviewRequestSerializer(data=data)
        req_serializer.is_valid(raise_exception=True)
        start_date = req_serializer.validated_data["start_date"]
        end_date = req_serializer.validated_data["end_date"]
        return start_date, end_date

    def init_data(self, request):
        # 校验
        start_date, end_date = self.verify_date(request.data)
        # 获取用户目录
        categories = Category.objects.filter(creator=request.user.username)
        # 获取时间内的所有事项
        items = Item.objects.filter(
            category_id__in=categories.values_list("id", flat=True),
            start_at__gte=start_date,
            start_at__lt=end_date + datetime.timedelta(days=1),
            archived=True,
        )
        return start_date, end_date, categories, items

    def init_response(self, data_map):
        data = []
        for category in data_map.values():
            if category["value"] < 1:
                continue
            category["duration_format"] = duration_format(category["value"])
            data.append(category)
        data.sort(key=lambda x: x["value"], reverse=True)
        return data

    def build_data_map(self, categories, category_map):
        temp_data = CategoryReadSerializer(instance=categories, many=True).data
        data_map = {category["id"]: category for category in temp_data}
        for category_id, category_map_data in category_map.items():
            data_map[category_id]["value"] = category_map_data["duration"]
        return data_map

    @action(methods=["POST"], detail=False)
    def full(self, request, *args, **kwargs):
        # 通用初始化
        start_date, end_date, categories, items = self.init_data(request)
        # 构造数据
        category_map = {
            category.id: {"instance": category, "duration": 0}
            for category in categories
        }
        # 为事项所在层级及以上层级添加时间
        for item in items:
            for node_id in category_map[item.category_id]["instance"].families:
                category_map[node_id]["duration"] += item.duration
        # 为序列化后的数据添加时间
        data_map = self.build_data_map(categories, category_map)
        # 处理响应数据
        data = self.init_response(data_map)
        return Response(data)

    @action(methods=["POST"], detail=False)
    def details(self, request, *args, **kwargs):
        # 通用初始化
        start_date, end_date, categories, items = self.init_data(request)
        # 为事项所在层级添加时间
        tmp = {}
        for item in items:
            if item.category_id in tmp.keys():
                tmp[item.category_id]["value"] += item.duration
            else:
                category = categories.get(id=item.category_id)
                serializer = CategoryReadSerializer(category)
                tmp[category.id] = serializer.data
                tmp[category.id]["value"] = item.duration
        data = self.init_response(tmp)
        return Response(data)

    @action(methods=["POST"], detail=False)
    def common(self, request, *args, **kwargs):
        # 通用初始化
        start_date, end_date, categories, items = self.init_data(request)
        # 构造数据
        category_map = {
            category.id: {"instance": category, "duration": 0}
            for category in categories
        }
        # 为事项顶级添加时间
        for item in items:
            node_id = category_map[item.category_id]["instance"].top_node.id
            category_map[node_id]["duration"] += item.duration
        # 为序列化后的数据添加时间
        data_map = self.build_data_map(categories, category_map)
        # 处理响应数据
        data = self.init_response(data_map)
        return Response(data)


class StatisticView(GenericViewSet):
    """统计信息"""

    queryset = Item.objects.all()

    @action(methods=["GET"], detail=False)
    def get_valid_year(self, request, *args, **kwargs):
        return Response(
            [{"label": year, "value": year} for year in STATISTIC_YEAR_CONFIG.keys()]
        )

    @action(methods=["POST"], detail=False)
    def info(self, request, *args, **kwargs):
        year = request.data.get("year")
        if year not in STATISTIC_YEAR_CONFIG.keys():
            raise OperationError("统计年份不合法")
        categories = STATISTIC_YEAR_CONFIG.get(year, [])
        data = {}
        for category in categories:
            handler = StatisticHandler.get_handler(category)
            if handler is None:
                continue
            tmp = handler(year, request, *args, **kwargs)()
            if tmp is None:
                continue
            data[category] = tmp
        return Response(data)
