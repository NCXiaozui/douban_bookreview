# 豆瓣热门书评爬虫
因为最近在学爬虫，本来也想写一个爬电影评分的，但是好像写这个都写烂了，就想换一个，然后自己看书也比较喜欢看看豆瓣书评，所以就写了一个爬虫的代码爬取豆瓣热门书评，可以爬取豆瓣热门书评。
因为是第一次写，还有一些问题没有解决，等我解决了，我再更新一下。
# 配置文件conf.py
在conf.py文件，你可以配置以下参数：

MAX_PAGES: 这个是爬取的最大网页数，是一个以0为底，20间隔的递增数。

HEADERS： 报头，这个你可以根据你自己的电脑自己修改。

SAVE_PATH: 文件保存路径。默认是项目的data下面。

# 输出格式：
json
字段：

bookname: 评论的书籍

title: 文章标题

author: 作者

attitude： 读者对文章的态度

ratingvalue: 作者对书籍的评分

content: 文章内容（只限文字部分，无配图）

# 爬取逻辑
1.main.py
采用线程池的方式抓取内容。通过队列让抓取与保存程序资源共享

2.spider
项目主要的爬虫代码

collect_url:
抓取热门书评的url

parse_review():
爬取对应的书评，解析相应的字段。

save_file():
保存文件函数

# 执行：
`python main.py`