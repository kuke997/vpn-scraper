# VPN节点爬虫

本项目实现了自动爬取、验证和更新VPN节点数据的功能，并通过API接口将数据传输到WEB8.4项目。

## 功能特点

- 支持从多种来源爬取VPN节点数据：
  - Telegram频道
  - GitHub仓库
  - 网站
- 自动验证节点可用性
- 标准化节点数据格式
- 通过API接口更新数据
- 支持代理轮换
- 完善的日志记录

## 安装

1. 克隆仓库
```bash
git clone <repository-url>
cd vpn_scraper
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建`.env`文件，添加以下内容：
```
# API配置
API_BASE_URL=https://cloakaccess.com/api
API_KEY=your-secret-api-key

# 爬虫配置
TELEGRAM_CHANNEL_1=https://t.me/vpnchannel1
GITHUB_REPO_1=https://github.com/vpnrepo/nodes
WEBSITE_1=https://example.com/free-vpn

# 代理配置
USE_PROXY=false
# PROXY_MAX_USES=5
# PROXY_TIMEOUT=300

# 验证器配置
VPN_VALIDATOR_TIMEOUT=5
VPN_VALIDATOR_PARALLEL=20

# SSL验证
VERIFY_SSL=true
```

## 使用方法

直接运行主程序：
```bash
python vpn_scraper.py
```

设置定时任务（Linux/Unix）：
```bash
# 编辑crontab
crontab -e

# 添加定时任务，每天凌晨2点执行
0 2 * * * cd /path/to/vpn_scraper && python vpn_scraper.py >> /var/log/vpn-scraper.log 2>&1
```

## 目录结构

```
/vpn_scraper/
├── vpn_scraper.py           # 主程序
├── config.py                # 配置文件
├── scrapers/                # 爬虫模块
│   ├── __init__.py
│   ├── base_scraper.py      # 爬虫基类
│   ├── telegram_scraper.py  # Telegram频道爬虫
│   ├── github_scraper.py    # GitHub仓库爬虫
│   └── website_scraper.py   # 网站爬虫
├── validators/              # 验证模块
│   ├── __init__.py
│   ├── node_validator.py    # 节点验证器
│   └── config_parser.py     # 配置解析器
├── utils/                   # 工具模块
│   ├── __init__.py
│   ├── proxy_rotator.py     # 代理轮换
│   ├── user_agents.py       # UA轮换
│   ├── geo_lookup.py        # 地理位置查询
│   └── api_client.py        # API客户端
├── data/                    # 数据存储目录
├── backups/                 # 备份目录
├── requirements.txt         # 依赖列表
└── README.md                # 说明文档
```

## 注意事项

- 请确保API密钥安全，不要将其硬编码或提交到版本控制系统中
- 定期轮换API密钥
- 如果使用代理，请确保代理服务器可靠
- 建议在服务器环境中运行，确保稳定的网络连接