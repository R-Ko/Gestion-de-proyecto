from typing import Optional

class Pagination:
    def __init__(self, page: int = 1, limit: int = 20):
        self.page = max(page, 1)
        self.limit = max(min(limit, 100), 1)

    def offset(self) -> int:
        return (self.page - 1) * self.limit

    def meta(self, total: int) -> dict:
        return {"page": self.page, "limit": self.limit, "total": total}
