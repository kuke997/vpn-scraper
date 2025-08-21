"""
VPN Scraper 验证模块初始化文件
"""

# 导入所有验证类
from .config_parser import ConfigParser
from .node_validator import NodeValidator

__all__ = [
    "ConfigParser",
    "NodeValidator"
]