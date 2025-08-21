import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # API配置
    API_BASE_URL = os.environ.get("API_BASE_URL", "https://cloakaccess.com/api")
    API_KEY = os.environ.get("API_KEY", "")
    
    # API请求配置
    API_TIMEOUT = int(os.environ.get("API_TIMEOUT", "30"))
    API_MAX_RETRIES = int(os.environ.get("API_MAX_RETRIES", "3"))
    
    # 代理配置
    USE_PROXY = os.environ.get("USE_PROXY", "false").lower() == "true"
    PROXY_MAX_USES = int(os.environ.get("PROXY_MAX_USES", "5"))
    PROXY_TIMEOUT = int(os.environ.get("PROXY_TIMEOUT", "300"))
    
    # 验证器配置
    VPN_VALIDATOR_TIMEOUT = int(os.environ.get("VPN_VALIDATOR_TIMEOUT", "5"))
    VPN_VALIDATOR_PARALLEL = int(os.environ.get("VPN_VALIDATOR_PARALLEL", "20"))
    
    # SSL验证
    VERIFY_SSL = os.environ.get("VERIFY_SSL", "true").lower() == "true"
    
    # Telegram配置
    TELEGRAM_CHANNELS = [
        os.environ.get("TELEGRAM_CHANNEL_1", "https://t.me/s/freevpn8"),
        os.environ.get("TELEGRAM_CHANNEL_2", "https://t.me/s/v2rayfree"),
        os.environ.get("TELEGRAM_CHANNEL_3", "https://t.me/s/ssrshares"),
    ]
    
    # GitHub配置
    GITHUB_REPOS = [
        os.environ.get("GITHUB_REPO_1", "https://github.com/freefq/free"),
        os.environ.get("GITHUB_REPO_2", "https://github.com/mianfeifq/share"),
        os.environ.get("GITHUB_REPO_3", "https://github.com/2dust/v2rayN/wiki/免费服务器"),
        os.environ.get("GITHUB_REPO_4", "https://github.com/Alvin9999/new-pac/wiki/v2ray免费账号"),
    ]
    
    # 网站配置
    WEBSITES = [
        os.environ.get("WEBSITE_1", "https://www.vpngate.net/en/"),
        os.environ.get("WEBSITE_2", "https://free-proxy-list.net/"),
        os.environ.get("WEBSITE_3", "https://proxyscrape.com/free-proxy-list"),
    ]