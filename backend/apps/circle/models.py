import math

from django.core.exceptions import MultipleObjectsReturned
from django.db import models, transaction

from constents import SHORT_CHAR_LENGTH, USERNAME_CHAR_LENGTH
from utils.exceptions import ServerError

DB_PREFIX = "circle_"


class Category(models.Model):
    """目录"""

    name = models.CharField("目录名", max_length=SHORT_CHAR_LENGTH)
    parent_id = models.BigIntegerField("父级ID", default=0)
    creator = models.CharField("创建者", max_length=USERNAME_CHAR_LENGTH)
    create_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = f"{DB_PREFIX}category"
        verbose_name = "目录"
        verbose_name_plural = verbose_name
        unique_together = [["name", "parent_id", "creator"]]
        ordering = ["-create_at"]

    def __str__(self):
        return self.name

    @transaction.atomic()
    def delete(self, using=None, keep_parents=False):
        Item.objects.filter(category_id=self.id).delete()
        children = Category.objects.filter(parent_id=self.id)
        for child in children:
            child.delete()
        return super().delete(using, keep_parents)

    @property
    def families(self):
        """从树的末端向上查找"""
        data = [self.id]
        if self.parent_id == 0:
            return data
        category = Category.objects.get(id=self.parent_id)
        data.extend(category.families)
        return data

    @property
    def top_node(self):
        """获取顶级目录"""
        if self.parent_id == 0:
            return self
        category = Category.objects.get(id=self.parent_id)
        return category.top_node


class ItemManager(models.Manager):
    def unfinished_item(self, username):
        category_ids = Category.objects.filter(creator=username).values_list(
            "id", flat=True
        )
        try:
            item = Item.objects.get(category_id__in=category_ids, archived=False)
        except Item.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            raise ServerError()
        return item


class Item(models.Model):
    """事项"""

    category_id = models.BigIntegerField("目录ID")
    start_at = models.DateTimeField("开始时间", auto_now_add=True)
    end_at = models.DateTimeField("结束时间", null=True)
    archived = models.BooleanField("存档状态", default=False)
    desc = models.CharField("描述信息", max_length=24, null=True, blank=True)

    objects = ItemManager()

    class Meta:
        db_table = f"{DB_PREFIX}circle"
        verbose_name = "事项"
        verbose_name_plural = verbose_name
        index_together = [["category_id", "start_at", "end_at"]]

    def __str__(self):
        category = Category.objects.get(id=self.category_id)
        return f"{category.name}:{self.start_at}:{self.end_at}"

    @property
    def duration(self):
        return math.ceil((self.end_at - self.start_at).total_seconds())
