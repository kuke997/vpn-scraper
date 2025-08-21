"""
VPN Scraper 爬虫模块初始化文件
"""

# 导入所有爬虫类
from .base_scraper import BaseScraper
from .telegram_scraper import TelegramScraper
from .github_scraper import GithubScraper
from .website_scraper import WebsiteScraper

__all__ = [
    "BaseScraper",
    "TelegramScraper",
    "GithubScraper",
    "WebsiteScraper"
]