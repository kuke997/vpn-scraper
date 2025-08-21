import os
import requests
import json
import logging
from datetime import datetime
import uuid
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import Config

class APIClient:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or Config.API_BASE_URL
        self.api_key = api_key or Config.API_KEY
        
        if not self.api_key:
            logging.warning("API key not provided. Authentication will fail.")
    
    def get_headers(self):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "VPN-Scraper/1.0"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        return headers
    
    def get_session(self):
        """创建一个带有重试策略的会话"""
        session = requests.Session()
        
        # 定义重试策略
        retry_strategy = Retry(
            total=Config.API_MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def update_vpn_nodes(self, nodes):
        """更新VPN节点数据"""
        endpoint = f"{self.base_url}/vpn/servers"
        
        # 格式化节点数据以符合API要求
        formatted_nodes = self._format_nodes_for_api(nodes)
        
        try:
            session = self.get_session()
            response = session.post(
                endpoint,
                headers=self.get_headers(),
                json=formatted_nodes,
                timeout=Config.API_TIMEOUT,
                verify=Config.VERIFY_SSL
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to update VPN nodes: {e}")
            self._save_backup(nodes)
            # 即使API调用失败，也不抛出异常，继续执行后续操作
            return {"success": False, "error": str(e)}
    
    def delete_vpn_nodes(self, node_ids):
        """删除指定ID的VPN节点"""
        endpoint = f"{self.base_url}/vpn/servers/delete"
        
        try:
            session = self.get_session()
            response = session.post(
                endpoint,
                headers=self.get_headers(),
                json={"node_ids": node_ids},
                timeout=Config.API_TIMEOUT,
                verify=Config.VERIFY_SSL
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to delete VPN nodes: {e}")
            # 即使API调用失败，也不抛出异常，继续执行后续操作
            return {"success": False, "error": str(e)}
    
    def clear_cache(self):
        """刷新API缓存"""
        endpoint = f"{self.base_url}/clear-cache/vpn"
        
        try:
            session = self.get_session()
            response = session.post(
                endpoint,
                headers=self.get_headers(),
                timeout=Config.API_TIMEOUT,
                verify=Config.VERIFY_SSL
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Failed to clear cache: {e}")
            return {"success": False, "error": str(e)}
    
    def _save_backup(self, data):
        """保存数据备份"""
        backup_dir = "./backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"vpn-nodes.{timestamp}.json")
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logging.info(f"Backup saved to {backup_file}")
    
    def _format_nodes_for_api(self, nodes):
        """将节点格式化为API期望的格式"""
        formatted_nodes = []
        
        for node in nodes:
            # 生成节点ID（如果不存在）
            node_id = node.get("id", str(uuid.uuid4()))
            
            # 构建translations字段
            translations = {
                "zh": {
                    "country": node.get("country", "未知"),
                    "type": node.get("type", "标准节点"),
                    "features": node.get("features", ["P2P"])
                },
                "en": {
                    "country": node.get("country_en", node.get("country", "Unknown")),
                    "type": node.get("type_en", node.get("type", "Standard Node")),
                    "features": node.get("features_en", node.get("features", ["P2P"]))
                }
            }
            
            # 构建符合API要求的节点对象
            formatted_node = {
                "id": node_id,
                "translations": translations,
                "speed": node.get("speed", "Unknown"),
                "load": node.get("load", 50),
                "lastUpdate": node.get("lastUpdate", datetime.now().isoformat()),
                "source": node.get("source", "爬虫"),
                "config": node.get("config", "")
            }
            
            formatted_nodes.append(formatted_node)
            
        return formatted_nodes