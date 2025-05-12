import time
import psutil
import logging
from prometheus_client import start_http_server, Gauge, Counter, Histogram
from config.config import Config

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 系統指標
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU 使用率百分比')
MEMORY_USAGE = Gauge('memory_usage_percent', '記憶體使用率百分比')
DISK_USAGE = Gauge('disk_usage_percent', '磁碟使用率百分比')
NETWORK_BYTES_SENT = Counter('network_bytes_sent', '已發送的網路流量')
NETWORK_BYTES_RECV = Counter('network_bytes_recv', '已接收的網路流量')

# 應用程式指標
REQUEST_COUNT = Counter('http_requests_total', 'HTTP 請求總數', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP 請求延遲時間', ['method', 'endpoint'])
ERROR_COUNT = Counter('http_errors_total', 'HTTP 錯誤總數', ['method', 'endpoint', 'error_type'])
ACTIVE_USERS = Gauge('active_users', '活躍使用者數量')
API_CALLS = Counter('api_calls_total', 'API 呼叫總數', ['endpoint'])
CACHE_HITS = Counter('cache_hits_total', '快取命中次數')
CACHE_MISSES = Counter('cache_misses_total', '快取未命中次數')

# 資料庫指標
DB_CONNECTIONS = Gauge('db_connections', '資料庫連線數量')
DB_QUERY_TIME = Histogram('db_query_duration_seconds', '資料庫查詢時間')
DB_ERRORS = Counter('db_errors_total', '資料庫錯誤總數')

# Redis 指標
REDIS_CONNECTIONS = Gauge('redis_connections', 'Redis 連線數量')
REDIS_MEMORY_USAGE = Gauge('redis_memory_usage_bytes', 'Redis 記憶體使用量')
REDIS_KEYS = Gauge('redis_keys', 'Redis 鍵值數量')

def collect_system_metrics():
    """收集系統指標"""
    try:
        # CPU 使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        CPU_USAGE.set(cpu_percent)
        
        # 記憶體使用率
        memory = psutil.virtual_memory()
        MEMORY_USAGE.set(memory.percent)
        
        # 磁碟使用率
        disk = psutil.disk_usage('/')
        DISK_USAGE.set(disk.percent)
        
        # 網路流量
        net_io = psutil.net_io_counters()
        NETWORK_BYTES_SENT.inc(net_io.bytes_sent)
        NETWORK_BYTES_RECV.inc(net_io.bytes_recv)
        
        logger.debug(f"系統指標收集完成: CPU={cpu_percent}%, MEM={memory.percent}%, DISK={disk.percent}%")
    
    except Exception as e:
        logger.error(f"收集系統指標時發生錯誤: {e}")

def collect_application_metrics():
    """收集應用程式指標"""
    try:
        # 這裡可以加入從應用程式收集指標的邏輯
        # 例如：從 Redis 或資料庫中讀取統計數據
        pass
    
    except Exception as e:
        logger.error(f"收集應用程式指標時發生錯誤: {e}")

def collect_database_metrics():
    """收集資料庫指標"""
    try:
        # 這裡可以加入從資料庫收集指標的邏輯
        # 例如：查詢資料庫連線數、查詢時間等
        pass
    
    except Exception as e:
        logger.error(f"收集資料庫指標時發生錯誤: {e}")

def collect_redis_metrics():
    """收集 Redis 指標"""
    try:
        # 這裡可以加入從 Redis 收集指標的邏輯
        # 例如：查詢 Redis 連線數、記憶體使用量等
        pass
    
    except Exception as e:
        logger.error(f"收集 Redis 指標時發生錯誤: {e}")

def start_monitoring():
    """啟動監控服務"""
    try:
        # 啟動 Prometheus 指標伺服器
        start_http_server(Config.PROMETHEUS_METRICS_PORT)
        logger.info(f"監控服務已啟動，監聽端口: {Config.PROMETHEUS_METRICS_PORT}")
        
        while True:
            try:
                collect_system_metrics()
                collect_application_metrics()
                collect_database_metrics()
                collect_redis_metrics()
                time.sleep(60)  # 每分鐘收集一次指標
            
            except Exception as e:
                logger.error(f"收集指標時發生錯誤: {e}")
                time.sleep(60)  # 發生錯誤時等待一分鐘後重試
    
    except Exception as e:
        logger.error(f"啟動監控服務時發生錯誤: {e}")
        raise

if __name__ == '__main__':
    try:
        start_monitoring()
    except KeyboardInterrupt:
        logger.info("監控服務已停止")
    except Exception as e:
        logger.error(f"監控服務異常終止: {e}")
        exit(1) 