from loguru import logger


# Логгирование
logger.add("logs/file_log.log", rotation="500 MB") 


# Параметры для работы с API
SHOP_ID = 5
SECRET_KEY = "SecretKey01"

class CurrencyCodes:
    '''
    Codes for currency piastrix API
    '''
    EUR = 978 
    USD = 840 
    RUB = 643