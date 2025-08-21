# VPN节点API使用指南

本文档详细描述了VPN节点爬虫项目如何与WEB8.4项目进行集成，以及API的使用方法。

## 项目概述

VPN节点爬虫项目是一个自动化工具，用于：
1. 从多个来源（Telegram、GitHub、网站）收集VPN节点信息
2. 验证节点的可用性和性能
3. 通过API将有效节点传输到WEB8.4项目
4. 管理节点的生命周期（添加、更新、删除）

## API集成说明

### 1. API端点配置

在项目根目录的`.env`文件中配置以下参数：

```
API_BASE_URL=https://cloakaccess.com/api
API_KEY=your-secret-api-key
```

### 2. 认证方式

API使用Bearer Token进行认证，在请求头中添加：

```
Authorization: Bearer your-secret-api-key
```

### 3. 主要API端点

#### 获取VPN节点
- **URL**: `GET /vpn/servers`
- **参数**: 可选参数`lang`指定语言（zh/en），默认为zh
- **响应**: 返回所有VPN节点数据

#### 更新VPN节点
- **URL**: `POST /vpn/servers`
- **请求体**: VPN节点数组
- **响应**: `{"success":true,"added":添加数量,"total":总数量}`

#### 删除VPN节点
- **URL**: `POST /vpn/servers/delete`
- **请求体**: `{"node_ids":["id1","id2",...]}` 
- **响应**: `{"success":true,"deleted":删除数量,"remaining":剩余数量}`

#### 缓存刷新
- **URL**: `POST /clear-cache/vpn`
- **响应**: 缓存刷新状态

### 4. 节点数据格式

传输到API的节点数据格式如下：

```json
{
  "id": "唯一标识符",
  "translations": {
    "zh": {
      "country": "国家名称",
      "type": "节点类型",
      "features": ["特性1", "特性2"]
    },
    "en": {
      "country": "Country Name",
      "type": "Node Type",
      "features": ["Feature 1", "Feature 2"]
    }
  },
  "speed": "速度信息",
  "load": 负载百分比,
  "lastUpdate": "最后更新时间",
  "source": "数据来源",
  "config": "节点配置"
}
```

## 使用方法

### 自动化运行

项目设计为自动化运行，可通过以下方式设置：

1. **直接运行**：
   ```bash
   python vpn_scraper.py
   ```

2. **测试模式**（不调用API）：
   ```bash
   python vpn_scraper.py --test
   ```

3. **定时任务**（Linux/Unix）：
   ```bash
   # 编辑crontab
   crontab -e

   # 添加定时任务，每小时执行一次
   0 * * * * cd /path/to/vpn_scraper && python vpn_scraper.py >> /var/log/vpn-scraper.log 2>&1
   ```

### 手动传输节点

如果需要手动传输节点数据，可以使用[simple_transfer.py](file:///e:/bf/VPNgithub/vpn_scraper/simple_transfer.py)脚本：

```bash
python simple_transfer.py
```

## 配置说明

### 环境变量

在`.env`文件中可以配置以下参数：

- `API_BASE_URL`: API基础URL
- `API_KEY`: API密钥
- `USE_PROXY`: 是否使用代理（true/false）
- `VPN_VALIDATOR_TIMEOUT`: 节点验证超时时间（秒）
- `VPN_VALIDATOR_PARALLEL`: 并行验证节点数
- `VERIFY_SSL`: 是否验证SSL证书（true/false）

### Telegram频道配置

```bash
TELEGRAM_CHANNEL_1=https://t.me/频道ID1
TELEGRAM_CHANNEL_2=https://t.me/频道ID2
```

### GitHub仓库配置

```bash
GITHUB_REPO_1=https://github.com/用户名/仓库名1
GITHUB_REPO_2=https://github.com/用户名/仓库名2
```

### 网站配置

```bash
WEBSITE_1=https://example.com/网站1
WEBSITE_2=https://example.com/网站2
```

## 故障排除

### 常见问题

1. **API认证失败**：
   - 检查API密钥是否正确配置
   - 确认API密钥未过期

2. **网络连接问题**：
   - 检查网络连接是否正常
   - 如果有防火墙，尝试启用代理配置

3. **节点验证失败**：
   - 检查节点验证超时设置
   - 调整并行验证节点数

### 日志查看

所有操作都会记录在[vpn_scraper.log](file:///e:/bf/VPNgithub/vpn_scraper/vpn_scraper.log)文件中，可以通过以下命令查看：

```bash
tail -f vpn_scraper.log
```

## 维护建议

1. **定期轮换API密钥**以确保安全性
2. **监控日志文件**以发现潜在问题
3. **定期检查代理配置**以确保网络连接稳定
4. **备份重要数据**以防意外丢失