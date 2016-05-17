# qcwy
 plus  
使用scrapy实现一个搜索并抓取前程无忧职位信息的爬虫

主要功能：通过提供的关键字、地区、行业、工作年限，搜索前程无忧上的职位，获取职位的相关信息

，并将其存入指定的MySQL库中。

使用方法：
1.在qwcy/qwcy/parameters.py中修改搜索参数  
2.修改qwcy/qwcy/db_setup.py中修改登录参数，并运行以创建数据库  
3.运行qwcy/run.bat，或调出cmd命令行输入scrapy crawl qcwysearch进行爬取  

原始爬虫的实现参考了：http://blog.csdn.net/peng00/article/details/48809591
  
但是该爬虫目前已不能正常使用。本爬虫在该基础上实现了更多功能上的创新。