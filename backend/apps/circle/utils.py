import datetime

from django.utils.module_loading import import_string

from apps.circle.models import Category, Item
from constents.statistic import (
    STATISTIC_EVENING_END_TIME,
    STATISTIC_EVENING_START_TIME,
    STATISTIC_MORNING_END_TIME,
    STATISTIC_MORNING_START_TIME,
    STATISTIC_RANK_COUNT,
)


class StatisticHandler:
    @classmethod
    def get_handler(cls, key: str):
        handler_name = f"apps.circle.utils.{key.lower().title()}StatisticHandler"
        try:
            return import_string(handler_name)
        except ImportError:
            return None


class StatisticHandlerBase:
    _categories_init = False
    categories = []
    category_map = {}
    items = []

    def __init__(self, year, request, *args, **kwargs):
        self.year = year
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self._init_first()

    def _init_first(self):
        """初始化"""
        self._init_year_range()
        self._init_categories()
        self._init_category_map()
        self._init_items()

    def _init_year_range(self):
        """初始化时间段"""
        self.start_date = datetime.datetime.strptime(
            f"{self.year}/1/1 00:00:00", "%Y/%m/%d %H:%M:%S"
        )
        self.end_date = datetime.datetime.strptime(
            f"{str(int(self.year) + 1)}/1/1 00:00:00", "%Y/%m/%d %H:%M:%S"
        )

    def _init_categories(self):
        """初始化目录"""
        self.categories = Category.objects.filter(creator=self.request.user.username)

    def _init_category_map(self):
        """初始化目录map"""
        self.category_map = {category.id: category for category in self.categories}

    def _init_items(self):
        """初始化事项"""
        self.items = Item.objects.filter(
            category_id__in=self.categories.values_list("id", flat=True),
            start_at__gte=self.start_date,
            start_at__lt=self.end_date,
            archived=True,
        )

    def plus_items_duration(self, items: list[Item]):
        """计算传入的 items 的累计时间"""
        duration = 0
        for item in items:
            duration += item.duration
        return duration

    def plus_item_group_by_category(self):
        """计算每个类别的总时间"""
        category_plus_map = {}
        for item in self.items:
            category_id = item.category_id
            if category_id in category_plus_map.keys():
                category_plus_map[category_id].append(item)
            else:
                category_plus_map[category_id] = [item]
        return {
            category_id: {
                "item_name": self.category_map[category_id].name,
                "item_record_count": len(items),
                "item_record_during": self.plus_items_duration(items),
                "items": items,
            }
            for category_id, items in category_plus_map.items()
        }

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class HomeStatisticHandler(StatisticHandlerBase):
    def __call__(self, *args, **kwargs):
        data = {
            "total_count": self.items.count(),
            "total_time": self.plus_items_duration(self.items),
        }
        return data


class EncounterStatisticHandler(StatisticHandlerBase):
    def get_max_item(self):
        max_category = {"item_record_during": 0, "items": []}
        category_plus_map = self.plus_item_group_by_category()
        for category in category_plus_map.values():
            if category["item_record_during"] > max_category["item_record_during"]:
                max_category = category
        days = set()
        days.update(
            [item.start_at.strftime("%Y/%m/%d") for item in max_category["items"]]
        )
        max_category["item_record_during"] = len(days)
        return max_category

    def __call__(self, *args, **kwargs):
        max_category = self.get_max_item()
        data = {
            "year": self.year,
            "item_name": max_category["item_name"],
            "item_record_count": max_category["item_record_count"],
            "item_record_during": max_category["item_record_during"],
        }
        return data


class MorningStatisticHandler(StatisticHandlerBase):
    def get_morning_item(self):
        items = self.items.filter(
            start_at__hour__gte=STATISTIC_MORNING_START_TIME,
            start_at__hour__lt=STATISTIC_MORNING_END_TIME,
        ).order_by("start_at__hour")
        if items.exists():
            return items.first()
        return None

    def __call__(self, *args, **kwargs):
        item = self.get_morning_item()
        if item is None:
            return None
        data = {
            "item_name": self.category_map[item.category_id].name,
            "item_duration": item.duration,
            "item_date": item.start_at.strftime("%m月%d日"),
            "start_at": item.start_at.strftime("%H:%M"),
        }
        return data


class EveningStatisticHandler(StatisticHandlerBase):
    def get_evening_item(self):
        items = self.items.filter(
            start_at__hour__gte=STATISTIC_EVENING_START_TIME,
            start_at__hour__lt=STATISTIC_EVENING_END_TIME,
        ).order_by("-start_at__hour")
        if items.exists():
            return items.first()
        return None

    def __call__(self, *args, **kwargs):
        item = self.get_evening_item()
        if item is None:
            return None
        data = {
            "item_name": self.category_map[item.category_id].name,
            "item_duration": item.duration,
            "item_date": item.start_at.strftime("%m月%d日"),
            "start_at": item.start_at.strftime("%H:%M"),
        }
        return data


class RankStatisticHandler(StatisticHandlerBase):
    def get_rank_items(self):
        category_plus_map = self.plus_item_group_by_category()
        ranked_items = [category for category in category_plus_map.values()]
        ranked_items.sort(key=lambda x: x["item_record_during"], reverse=True)
        return ranked_items[:STATISTIC_RANK_COUNT]

    def __call__(self, *args, **kwargs):
        ranked_items = self.get_rank_items()
        data = [
            {"name": item["item_name"], "duration": item["item_record_during"]}
            for item in ranked_items
        ]
        return data
