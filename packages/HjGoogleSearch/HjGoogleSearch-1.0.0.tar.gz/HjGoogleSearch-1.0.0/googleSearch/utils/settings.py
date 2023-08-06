import redis
from pathlib import Path
from typing import Optional
from dynaconf import loaders, settings
from googleSearch.utils.logger import logger

DEFAULT_PATH = "settings.toml"
BASE_SETTINGS = {
    "IS_DEVE": True,
    "BASE_URL": "https://www.google.com",
    "HOME_DIR": str(Path().absolute()),
    "REDIS": {
        "HOST": 'localhost',
        "PORT": 6379,
        "DB": 4,
        "PASSWD": ""
    },
    "MYSQL": {
        "HOST": "",
        "USER": "",
        "PASSWD": "",
        "DATABASE": "",
        "PORT": 3306
    },
    'PROXY_USER': '',  # 代理用户名
    'PROXY_PWD': '',  # 代理密码
    "USER_AGENT": [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
    ],
    'EMAIL_EXISTS': ['admin@', 'sales@', 'team@', 'support@', 'customercare@', 'info@', 'customer@', 'service@',
                     'contact@', 'hello@'],
    'EXCLUDE_KEY_WORD': ['walmart.', 'sendo.', 'aliexpress.', 'wish.', 'amazon.', 'lazada.', 'ebay.', 'google.',
                         'shopee',
                         'tokopedia.', 'zipy.', 'tiki.', 'imall.', 'amazon.co.', 'joom.', 'dhgate.', 'taobao.',
                         'tmall.',
                         'jd.', 'suning.', 'zipy.', '1688.', 'pinterest', 'facebook.', 'youtube.', 'adobe.com', 'etsy.',
                         'alibaba.', 'vimeo.', 'tistory.', 'heavy.', 'line.', 'buzzfeed.', 'kijiji.', 'gearbest.',
                         'bonanza.', 'staples.', 'jimmyjazz.', 'sunsky-online.', 'pcwonderland.', 'pnghut.',
                         'aliradar.', 'pricecheck.', 'allmacworld.', 'wanelo.', 'findniche.', 'ecomhunt.', 'amz520.',
                         'jiwaji.'],
    'TOTAL_PAGE': 10,  # 期望爬取的页数
    # redis相关key
    # 用户输入AE url爬取初始数据
    'URL_FOR_CRAWL_AE_REDIS_KEY': 'URL_FOR_CRAWL_AE',
    # 上传图片后获取带sbi的链接
    'URL_WITH_SBI': 'URL_WITH_SBI',
    # GOOGLE搜索过滤后最终结果存入redis
    'GOOGLE_SEARCH_RESULT_REDIS_KEY': 'GOOGLE_SEARCH_RESULT'
}


def load_or_create_settings(path: Optional[str]):
    path = path or DEFAULT_PATH
    if not Path(path).exists():
        default_settings_path = str(Path.cwd() / Path(DEFAULT_PATH))
        logger.info(
            f'没有发现配置文件 "{Path(path).absolute()}". '
            f"创建默认配置文件: {default_settings_path}",
        )
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        loaders.write(default_settings_path, BASE_SETTINGS, env="default")
    settings.load_file(path=path)
    logger.info("配置文件加载成功")
