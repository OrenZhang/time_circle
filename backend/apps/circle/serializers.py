from rest_framework import serializers

from apps.circle.models import Category, Item


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
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        exclude = ["creator", "parent_id"]

    def get_parent_category(self, parent_id: int):
        category = Category.objects.get(id=parent_id)
        if category.parent_id == 0:
            return category.name
        return "{}/{}".format(
            self.get_parent_category(category.parent_id), category.name
        )

    def get_full_name(self, instance: Category):
        if instance.parent_id == 0:
            return instance.name
        return "{}/{}".format(
            self.get_parent_category(instance.parent_id), instance.name
        )


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemStopSerializer(serializers.Serializer):
    end_at = serializers.DateTimeField(required=True, allow_null=False)


class OverviewRequestSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(required=True, allow_null=False)
    end_date = serializers.DateTimeField(required=True, allow_null=False)


class OverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
