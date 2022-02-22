from django.db import models, transaction

from constents import SHORT_CHAR_LENGTH, USERNAME_CHAR_LENGTH

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
        return super().delete(using, keep_parents)


class Item(models.Model):
    """事项"""

    category_id = models.BigIntegerField("目录ID")
    start_at = models.DateTimeField("开始时间")
    end_at = models.DateTimeField("结束时间")
    archived = models.BooleanField("存档状态", default=False)
    create_at = models.DateTimeField("创建时间", auto_now_add=True)
    ordering = ["-create_at"]

    class Meta:
        db_table = f"{DB_PREFIX}circle"
        verbose_name = "事项"
        verbose_name_plural = verbose_name
        index_together = [["category_id", "start_at", "end_at"]]

    def __str__(self):
        category = Category.objects.get(id=self.category_id)
        return f"{category.name}:{self.start_at}:{self.end_at}"
