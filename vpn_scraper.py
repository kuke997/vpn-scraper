import sys
import os
import json
import logging
from datetime import datetime
import requests
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
load_dotenv()

# 导入项目模块
from scrapers.telegram_scraper import TelegramScraper
from scrapers.github_scraper import GithubScraper
from scrapers.website_scraper import WebsiteScraper
from validators.node_validator import NodeValidator
from utils.api_client import APIClient
from utils.proxy_rotator import ProxyRotator
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vpn_scraper.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def load_nodes_from_backup():
    """从备份文件加载节点数据"""
    backup_dir = "./backups"
    if not os.path.exists(backup_dir):
        return []
    
    backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.json')]
    if not backup_files:
        return []
    
    # 选择最新的备份文件
    latest_backup = max(backup_files)
    backup_path = os.path.join(backup_dir, latest_backup)
    
    try:
        with open(backup_path, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        logger.info(f"Loaded {len(nodes)} nodes from backup {latest_backup}")
        return nodes
    except Exception as e:
        logger.error(f"Failed to load nodes from backup: {e}")
        return []

def main(test_mode=False):
    logger.info("Starting to scrape VPN nodes...")
    
    try:
        # 初始化代理轮换器
        proxy_rotator = ProxyRotator()
        logger.info(f"Proxy status: {'enabled' if Config.USE_PROXY else 'disabled'}")
        
        # 初始化爬虫
        telegram_scraper = TelegramScraper(proxy_rotator)
        github_scraper = GithubScraper(proxy_rotator)
        website_scraper = WebsiteScraper(proxy_rotator)
        
        # 存储所有节点
        all_nodes = []
        
        # 1. 爬取Telegram频道
        for i, channel_url in enumerate(Config.TELEGRAM_CHANNELS, 1):
            try:
                logger.info(f"Scraping Telegram channel: {channel_url}")
                nodes = telegram_scraper.scrape(channel_url)
                logger.info(f"Scraped {len(nodes)} nodes from Telegram VPN Channel {i}")
                all_nodes.extend(nodes)
            except Exception as e:
                logger.error(f"Error scraping Telegram channel {channel_url}: {e}")
        
        # 2. 爬取GitHub仓库
        for i, repo_url in enumerate(Config.GITHUB_REPOS, 1):
            try:
                logger.info(f"Scraping GitHub repository: {repo_url}")
                nodes = github_scraper.scrape(repo_url)
                logger.info(f"Scraped {len(nodes)} nodes from GitHub VPN Repo {i}")
                all_nodes.extend(nodes)
            except Exception as e:
                logger.error(f"Error scraping GitHub repository {repo_url}: {e}")
        
        # 3. 爬取网站
        for i, website_url in enumerate(Config.WEBSITES, 1):
            try:
                logger.info(f"Scraping website: {website_url}")
                nodes = website_scraper.scrape(website_url)
                logger.info(f"Scraped {len(nodes)} nodes from Website VPN Source {i}")
                all_nodes.extend(nodes)
            except Exception as e:
                logger.error(f"Error scraping website {website_url}: {e}")
        
        logger.info(f"Total raw nodes: {len(all_nodes)}")
        
        # 4. 验证节点
        logger.info("Validating nodes...")
        validator = NodeValidator()
        valid_nodes = validator.validate_multiple(all_nodes)
        logger.info(f"Total validated nodes: {len(valid_nodes)}")
        
        # 5. 保存节点到文件
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"vpn_nodes_{timestamp}.json"
        filepath = os.path.join(data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(valid_nodes, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {len(valid_nodes)} nodes to {filepath}")
        
        # 6. 评估节点健康状况
        logger.info("Assessing node health...")
        healthy_nodes = []
        nodes_to_delete = []
        
        for node in valid_nodes:
            # 简单的健康评估逻辑
            # 在实际应用中，可能需要更复杂的健康检查
            if node.get("ping", 1000) < 500 and node.get("load", 100) < 90:
                healthy_nodes.append(node)
            else:
                nodes_to_delete.append(node.get("id"))
        
        logger.info(f"Healthy nodes: {len(healthy_nodes)}, Nodes to delete: {len(nodes_to_delete)}")
        
        if not test_mode:
            # 7. 初始化API客户端
            api_client = APIClient()
            
            # 8. 更新节点数据
            if healthy_nodes:
                logger.info("Updating nodes via API...")
                try:
                    result = api_client.update_vpn_nodes(healthy_nodes)
                    logger.info(f"API update result: {result}")
                except Exception as e:
                    logger.error(f"Failed to update VPN nodes: {e}")
                    # 保存备份以防API调用失败
                    api_client._save_backup(healthy_nodes)
            
            # 9. 删除不健康的节点
            if nodes_to_delete:
                logger.info(f"Deleting {len(nodes_to_delete)} unhealthy nodes...")
                try:
                    delete_result = api_client.delete_vpn_nodes(nodes_to_delete)
                    logger.info(f"Node deletion result: {delete_result}")
                except Exception as e:
                    logger.error(f"Failed to delete VPN nodes: {e}")
            
            # 10. 刷新API缓存
            logger.info("Clearing API cache...")
            try:
                cache_result = api_client.clear_cache()
                logger.info(f"Cache clear result: {cache_result}")
            except Exception as e:
                logger.error(f"Failed to clear cache: {e}")
        else:
            logger.info("Test mode: skipping API communication")
        
        logger.info("VPN node update completed successfully")
        
    except Exception as e:
        logger.error(f"Scraper failed with error: {e}")
        raise

if __name__ == "__main__":
    # 检查命令行参数
    test_mode = "--test" in sys.argv
    main(test_mode=test_mode)