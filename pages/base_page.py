import re

from playwright.sync_api import Page, expect

from config.settings import BASE_URL
from utils.allure_helpers import step

# Time to wait for slow, server-driven UI feedback (notifications, redirects)
FEEDBACK_TIMEOUT_MS = 10_000


class BasePage:
    PATH: str | None = None
    TITLE: str | None = None

    def __init__(self, page: Page):
        self.page = page
        self.page_title = (
            page.get_by_role("heading", name=self.TITLE, exact=True)
            if self.TITLE
            else None
        )

    @classmethod
    def absolute_url(cls) -> str:
        if cls.PATH is None:
            raise ValueError(f"{cls.__name__} has no PATH of its own")

        return f"{BASE_URL.rstrip('/')}{cls.PATH}"

    @step("Open page {self.PATH}")
    def open(self) -> None:
        self.page.goto(self.absolute_url())

    def get_title(self) -> str:
        return self.page.title()

    def _url_pattern(self) -> re.Pattern:
        base = re.escape(self.absolute_url().rstrip("/"))

        return re.compile(rf"^{base}/?(\?.*)?$")

    def is_opened(self) -> bool:
        return self._url_pattern().match(self.page.url) is not None

    def expect_opened(self) -> None:
        if self.PATH is not None:
            expect(self.page).to_have_url(self._url_pattern())

        if self.page_title is not None:
            expect(self.page_title).to_be_visible()
