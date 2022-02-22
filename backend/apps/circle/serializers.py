from rest_framework import serializers

from apps.circle.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_parent_id(self, value):
        if value == 0:
            return value
        try:
            Category.objects.get(id=value)
            return value
        except Category.DoesNotExist:
            raise serializers.ValidationError("父级目录不存在")


class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["creator"]
