import json
import os
from datetime import datetime


class JsonPipeline:
    """Export items to JSON files under data/."""

    def __init__(self):
        self.items = []
        self.filepath = None

    def open_spider(self, spider):
        os.makedirs("data", exist_ok=True)
        self.filepath = f"data/{spider.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def close_spider(self, spider):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item
