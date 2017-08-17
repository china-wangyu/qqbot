# coding:utf-8

import requests, urllib2
import qqmysql

from bs4 import BeautifulSoup


# 核心代码
# qqBotSlot

class QQAntSpider(object):
    """
        创建爬虫类
    """

    def __init__(self, key_words=''):
        self.param = {
            "url": "http://www.doutula.com/article/list/?page=",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
            },
        }
        self.key_words = key_words
        self.result = self.next_page()

    def loading(self,num = 0):
        """
        加载网页
        :param data: 网页header和url
        :return: 爬取的网页源代码
        """
        if self.key_words == "笑话":
            self.param['url'] = "http://www.qiushibaike.com/8hr/page/"+ str(num)
            request = urllib2.Request(url=self.param['url'], headers=self.param['headers'])
            contect = urllib2.urlopen(request)
            boday = contect.read()
            result = self.get_xiaohua_result(boday)
        elif self.key_words == "美女":
            self.param['url'] = "http://www.mmjpg.com/home/"+str(num)
            request = urllib2.Request(url=self.param['url'], headers=self.param['headers'])
            contect = urllib2.urlopen(request)
            boday = contect.read()
            result = self.get_xiaohua_result(boday)
        elif self.key_words == "斗图":
            self.param['url'] = "https://www.duitang.com/search/?kw=%E6%96%97%E5%9B%BE&type=feed#!s-p"+str(num)
            request = urllib2.Request(url=self.param['url'], headers=self.param['headers'])
            contect = urllib2.urlopen(request)
            boday = contect.read()
            result = self.get_xiaohua_result(boday)

        return result

    # 获取多页
    def next_page(self, num=10):
        """

        :param url: 爬去网页url
        :param num: 下载的页数
        :param src: 图片
        :return:
        """
        for i in range(1, num):
            print "正在进入第", i + 1, '页'
            result = self.loading(num+1)
            return result

    def get_xiaohua_result(self, boday):
        """
        获取翻译内容                    #div[class="output-bd"] > div[class='clearfix'] > span
        :param boday: 百度翻译内容
        :return: 翻译结果 类型：str
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
        return result


if __name__ == '__main__':
    QQAnt = QQAntSpider('笑话')
    QQMsql = qqmysql.QQMsql()
    QQ_Key = QQMsql.Table('qq_keywords')
    key_count = QQ_Key.select().where(QQ_Key.key_words == '笑话')
    for aut, cnt in zip(QQAnt.result['auth'], QQAnt.result['cont']):
        QQ_Key.create(key_words='笑话', result_url=QQAnt.param['url'], result_auth=aut, result_content=cnt)