# -*- coding: utf-8 -*-

# Scrapy settings for qcwy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'qcwy'

SPIDER_MODULES = ['qcwy.spiders']
NEWSPIDER_MODULE = 'qcwy.spiders'

#DUPEFILTER_DEBUG = 'True'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qcwy (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'qcwy.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'qcwy.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'qcwy.pipelines.QcwyJsonPipeline': 300,
	'qcwy.pipelines.QcwyMySQLPipeline': 800,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

#搜索参数
#同一属性两个条件联合用逗号分隔
KEYWORD = {
           'jobarea': '020000,030200,010000,040000,080200,00',   #北上广深杭
           'industrytype': '00',   #32表示互联网，42银行，03证券/金融，43保险, 00全体
           'keyword': '数据分析',
           'workyear': '99',        #99表示所有，01无经验，02一到三年，03三到五年，04五到十年
            }


#所需要的搜索的技能表，key为技能名，value为对应正则表达式
SKILLS = {
        'has_excel': 'excel',
        'has_mining': u'数据挖掘',
        'has_python': 'python',
        'has_hadoop': 'Hadoop',
        'has_hive': 'HIVE',
        'has_sql': 'SQL',
        'has_sas': 'SAS',
        'has_spss': 'SPSS',
        'has_java': 'java',
        'has_GA': 'Google Analytics|GA',
        'has_crawler': u'爬虫',
        'has_ETL': u'数据仓库|ETL',
        'has_R': u'R语言|(([\u4e00-\u9fa5]|\uff0c|\u3001|/|\\\\)R([\u4e00-\u9fa5]|\uff0c|\u3001|/|\\\\))',
        'has_mlearning': u'机械学习|scikit',
        'has_modeling': u'建模|数学模型',
        'has_algorithm': u'算法',
        'has_visialize': u'可视化|tableau'
        }
 
#输入你的登录名与密码 
FORMDATA = {'username': 'name', 'userpwd': 'password'}

#数据库名称与表名
DATABASE = {
            'user': 'root', 
            'password': 'password', 
            'host': 'localhost',
            'name': 'job_project',
            'table': 'alljobs'
            }