import logging
import logging.handlers
import os
from config.config import Config

def setup_logger(name):
    """設定應用程式日誌"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # 建立日誌目錄
    log_dir = os.path.dirname(Config.LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)
    
    # 檔案處理器 - 使用 RotatingFileHandler 進行日誌輪替
    file_handler = logging.handlers.RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
    
    # 控制台處理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
    
    # 加入處理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 建立應用程式日誌記錄器
app_logger = setup_logger('app')
db_logger = setup_logger('database')
api_logger = setup_logger('api')
auth_logger = setup_logger('auth')

def log_error(error, context=None):
    """記錄錯誤"""
    error_msg = f"Error: {str(error)}"
    if context:
        error_msg += f", Context: {context}"
    app_logger.error(error_msg)

def log_info(message, context=None):
    """記錄資訊"""
    info_msg = message
    if context:
        info_msg += f", Context: {context}"
    app_logger.info(info_msg)

def log_warning(message, context=None):
    """記錄警告"""
    warning_msg = message
    if context:
        warning_msg += f", Context: {context}"
    app_logger.warning(warning_msg)

def log_debug(message, context=None):
    """記錄除錯資訊"""
    debug_msg = message
    if context:
        debug_msg += f", Context: {context}"
    app_logger.debug(debug_msg) 