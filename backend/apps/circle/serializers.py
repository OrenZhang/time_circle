from rest_framework import serializers

from apps.circle.models import Category, Item
from utils.tools import duration_format


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


class ItemListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    duration_format = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"

    def get_parent_category(self, parent_id: int):
        category = Category.objects.get(id=parent_id)
        if category.parent_id == 0:
            return category.name
        return "{}/{}".format(
            self.get_parent_category(category.parent_id), category.name
        )

    def get_full_name(self, item: Item):
        try:
            instance = Category.objects.get(id=item.category_id)
        except Category.DoesNotExist:
            return None
        if instance.parent_id == 0:
            return instance.name
        return "{}/{}".format(
            self.get_parent_category(instance.parent_id), instance.name
        )

    def get_name(self, item: Item):
        try:
            return Category.objects.get(id=item.category_id).name
        except Category.DoesNotExist:
            return None

    def get_duration(self, item: Item):
        return item.duration

    def get_duration_format(self, item: Item):
        return duration_format(item.duration)


class ItemStopSerializer(serializers.Serializer):
    start_at = serializers.DateTimeField(required=True, allow_null=False)
    end_at = serializers.DateTimeField(required=True, allow_null=False)


class OverviewRequestSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(required=True, allow_null=False)
    end_date = serializers.DateTimeField(required=True, allow_null=False)

    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError("结束日期应大于等于开始日期")
        return attrs


class OverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
