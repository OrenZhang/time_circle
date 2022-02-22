from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.circle.models import Category
from apps.circle.serializers import CategoryReadSerializer, CategorySerializer


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
        return Response(serializer.data)  # 重写成树方法

    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response()
