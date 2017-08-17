# coding:utf-8

import requests, urllib2
import qqmysql
import load
import time

from bs4 import BeautifulSoup


# 核心代码
# qqBotSlot

class QQAntSpider(object):
    """
        创建爬虫类
    """

    def __init__(self, key_words='',num=10):
        self.param = {
            "url": "http://www.doutula.com/article/list/?page=",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
            },
        }
        self.key_words = key_words
        self.next_page(num)

    def loading(self,num = 0):
        """
        加载网页
        :param data: 网页header和url
        :return: 爬取的网页源代码
        """
        if self.key_words == "笑话":
            self.param['url'] = "https://www.qiushibaike.com/8hr/page/%s/" % str(num)
            request = urllib2.Request(url=self.param['url'], headers=self.param['headers'])
            contect = urllib2.urlopen(request)
            boday = contect.read()
            result = self.get_xiaohua_result(boday)
        elif self.key_words == "美女":
            self.param['url'] = "http://www.mmjpg.com/home/%s"%str(num)
            request = urllib2.Request(url=self.param['url'], headers=self.param['headers'])
            contect = urllib2.urlopen(request)
            boday = contect.read()
            result = self.get_meinv_result(boday)
        elif self.key_words == "斗图":
            # url参数
            self.param['url'] = "https://www.duitang.com/search/?kw=%E6%96%97%E5%9B%BE&type=feed"
            payload = {
                "start": num
            }
            request = requests.get(url=self.param['url'], params=payload, headers=self.param['headers'])
            contect = request.content
            result = self.get_doutu_result(contect)
        elif self.key_words == "段子":
            # url参数
            self.param['url'] = "http://neihanshequ.com/?page=%s" %num
            request = urllib2.Request(url=self.param['url'], headers=self.param['headers'])
            contect = urllib2.urlopen(request)
            boday = contect.read()
            result = self.get_duanzi_result(boday)
        elif self.key_words == "荤段子":
            # url参数
            self.param['url'] = "http://www.youquba.net/hsxh/list_33_%s.html" %num
            request = urllib2.Request(url=self.param['url'], headers=self.param['headers'])
            contect = urllib2.urlopen(request)
            boday = contect.read()
            result = self.get_hunduanzi_result(boday)
        return result

    # 获取多页
    def next_page(self, num=10):
        """

        :param url: 爬去网页url
        :param num: 下载的页数
        :param src: 图片
        :return:
        """
        result_list = []
        for i in range(1, num):
            print "正在进入第", i , '页'
            result = self.loading(i+1)
            result_list.append(result)
        return result


    def get_xiaohua_result(self, boday):
        """
        获取笑话                    #div[class="output-bd"] > div[class='clearfix'] > span
        :param boday: 获取的页面
        :return: 笑话集合
        """
        soup = BeautifulSoup(boday, "lxml")
        author_list = soup.select('a[rel="nofollow"] > img')  # 作者名称—集合
        auth_list = []
        for auth in author_list:
            try:
                auth_list.append(auth['alt'])
            except KeyError:
                auth_list.append('无名')

        content_list = soup.select('a[class="contentHerf"] > div[class=content] > span ')  # content—集合
        cont_list = []
        for cont in content_list:
            cont_list.append(cont.get_text().strip())


        result = {
            'auth': auth_list,
            'cont': cont_list,
        }
        int = self.add_table_sql(result)
        return int

    def get_meinv_result(self,boday):
        """
        获取妹子图
        :param boday: 获取的页面
        :return: 数据列表
        """
        soup = BeautifulSoup(boday, "lxml")
        loads = load.Load()
        author_list = soup.select('div[class="pic"] > ul > li > a > img')
        auth_list = [] #title集合
        cont_list = [] #图片集合
        for auth in author_list:
            try:
                auth_list.append(auth['alt'])
                host_path = loads.save_img("G:\python\img\meinv",auth['src'])
                cont_list.append(auth['src'])
            except KeyError:
                auth_list.append('无名')
                cont_list.append("没图")

        result = {
            'auth': auth_list,
            'cont': cont_list,
        }
        int = self.add_table_sql(result)
        return int

    def get_doutu_result(self,boday):
        """
        获取斗图
        :param boday: 获取的页面
        :return: 斗图集合
        """
        soup = BeautifulSoup(boday, "lxml")
        loads = load.Load()
        author_list = soup.select('div[class="j"] > div[class="wooscr"] > ul > li > p > a[class="p"]')
        auth_list = [] #title集合
        cont_list = [] #图片集合
        for auth in author_list:
            try:
                auth_list.append(auth.get_text().strip())
            except KeyError:
                auth_list.append('无名')

        img_list = soup.select('div[class="j"] > div[class="mbpho"] > a[class="a"] > img ')
        for img in img_list:
            try:
                host_path = loads.save_img("G:\python\img\meinv",img['src'])
                cont_list.append(img['src'])
            except KeyError:
                cont_list.append("没图")
        result = {
            'auth': auth_list,
            'cont': cont_list,
        }
        int = self.add_table_sql(result)
        return int

    def get_duanzi_result(self,boday):
        """
        获取段子记录
        :param boday: 段子页面
        :return: 段子集合
        """
        soup = BeautifulSoup(boday, "lxml")

        author_list = soup.select('span[class="name"]')
        auth_list = []  # title集合
        cont_list = []  # 图片集合
        for auth in author_list:
            try:
                auth_list.append(auth.get_text().strip())
            except KeyError:
                auth_list.append('无名')
        content_list = soup.select('div[class="content-wrapper"] > a > div > p')
        for cont in content_list:
            try:
                cont_list.append(cont.get_text().strip())
            except KeyError:
                cont_list.append('没有内容')
        result = {
            'auth': auth_list,
            'cont': cont_list,
        }
        int = self.add_table_sql(result)
        return int

    def get_hunduanzi_result(self,boday):
        """
        获取段子记录
        :param boday: 段子页面
        :return: 段子集合
        """
        soup = BeautifulSoup(boday, "lxml")
        author_list = soup.select('div[class="jokebox"] > div[class="jokebox_title"] > h3 > a')
        auth_list = []  # title集合
        cont_list = []  # 图片集合
        for auth in author_list:
            try:
                auth_list.append(auth.get_text().strip())
            except KeyError:
                auth_list.append('无名')

        content_list = soup.select('div[class="jokebox"] > p')
        for cont in content_list:
            try:
                cont_list.append(cont.get_text().strip())
            except KeyError:
                cont_list.append('没有内容')

        result = {
            'auth': auth_list,
            'cont': cont_list,
        }
        int = self.add_table_sql(result)
        return int

    def add_table_sql(self,result):
        """
        添加搜索记录进入数据表
        :param result: 数据集
        :return:bloone
        """
        QQMsql = qqmysql.QQMsql()
        QQ_Key = QQMsql.Table('qq_keywords')
        x = 0
        for aut, cnt in zip(result['auth'], result['cont']):
            str = ("正在添加第 %s 条数据,其作者为：%s" ) % (x,aut)
            time.sleep(1)  # 让爬虫休息1秒
            QQ_Key.create(key_words=self.key_words, result_url=self.param['url'], result_auth=aut, result_content=cnt)
            x = x+1
        return True

if __name__ == '__main__':
    # QQAnt = QQAntSpider('笑话')
    QQAnt = QQAntSpider('段子')
    # QQAnt = QQAntSpider('荤段子')