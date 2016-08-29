# qcwy
_plus
***

## 简述  
使用scrapy实现一个搜索并抓取前程无忧职位信息的爬虫

主要功能：通过提供的关键字、地区、行业、工作年限，搜索前程无忧上的职位，获取职位的相关信息，并将其存入指定的MySQL库中。
原始爬虫的实现参考了：http://blog.csdn.net/peng00/article/details/48809591
  
但是该爬虫目前已不能正常使用。本爬虫在该基础上实现了更多功能。


## 软件环境
python==2.7.10  
SQLAlchemy==1.0.13  
MySQL Server==5.6


## 使用方法：  
1. 在qwcy/qwcy/settings.py中修改搜索参数,51jobs登录参数和MySQL的数据库信息 
2. 运行qwcy/run.bat，或调出cmd命令行输入scrapy crawl qcwysearch进行爬取
3. 在qwcy/qwcy目录中找到json格式的搜索结果qcwy.json文件，或登入MySQL查询


## 最后
如有疑问可以邮件我dante3@126.com，谢谢！
