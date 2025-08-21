"""
VPN Scraper 工具模块初始化文件
"""

# 导入所有工具类
from .api_client import APIClient
from .geo_lookup import GeoLookup
from .proxy_rotator import ProxyRotator
from .user_agents import UserAgents

# 兼容旧版本导入
def get_random_user_agent():
    return UserAgents().random()

__all__ = [
    "APIClient",
    "GeoLookup",
    "ProxyRotator",
    "UserAgents",
    "get_random_user_agent"
]