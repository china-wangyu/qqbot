# coding:utf-8

# 导入模板
import peewee


class QQMsql(object):
    def __init__(self):
        self.param = {
            'host': "localhost",
            'dbname': 'qq',
            'user': 'root',
            'passwd': 'root',
            'port': 3306,
        }
        self.conn = peewee.MySQLDatabase(
            host=self.param['host'],
            port=self.param['port'],
            user=self.param['user'],
            passwd=self.param['passwd'],
            database=self.param['dbname']
        )

    def Table(self,table='qq_keywords'):
        class Qq_keywords(peewee.Model):
            key_words = peewee.CharField(max_length=200)
            result_url = peewee.CharField(max_length=255)
            result_auth = peewee.CharField(max_length=30)
            result_content = peewee.TextField()


            class Meta:
                database = self.conn

        return Qq_keywords

