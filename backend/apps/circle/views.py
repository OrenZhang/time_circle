from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from apps.circle.models import Category, Item
from apps.circle.serializers import (
    CategoryReadSerializer,
    CategorySerializer,
    ItemSerializer,
    ItemStopSerializer,
)
from utils.exceptions import Error404, OperationError, ParamsNotFound, PermissionDenied


class CategoryView(ModelViewSet):
    """目录"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryReadSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(creator=request.user)
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

    @action(methods=["GET"], detail=False)
    def tree(self, request, *args, **kwargs):
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


class ItemView(mixins.CreateModelMixin, GenericViewSet):
    """事项"""

    queryset = Item.objects.filter(archived=False)
    serializer_class = ItemSerializer

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
        if end_at <= instance.start_at:
            raise OperationError("结束时间需要大于开始时间")
        instance.end_at = end_at
        instance.archived = True
        instance.save()
        return Response()
