# coding:utf-8

#导入QQ模板
import qqbot
import qqmysql
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#核心代码
#qqBotSlot

@qqbot.QQBotSlot
def onQQMessage(bot,contact,member,content):
    """
        bot qq对象
        contact 发消息的人
        member 发消息的对象，这个只有在群里面的时候才会有参数
        content 发送的内容
    """
    print("bot:%s" % bot)
    print("contact:%s" % contact)
    print("member:%s" % member)
    print("content:%s" % content)



    if "@ME" in content:
        cont = content.rsplit(" ", 1)[-1]
        if "伤心" == cont:
            bot.SendTo(contact,"/微笑,怎么了？")
        elif "小仙女" == cont:
            bot.SendTo(contact,"/可爱 本仙女初来凡尘，凡尘处处都是本仙女名称！")
        elif "你是不是傻" == cont:
            bot.SendTo(contact,"/手枪 你有权保持沉默，你所说的一切都将被作为存盘记录。你可以请代理服务器，如果请不起网络会为你分配一个!")
        elif "小白兔" == cont:
            bot.SendTo(contact, '/卖萌 初音ミク/Hatsune Miku只是个机器人宝宝，小白兔是什么呢？')
        elif "停止" == cont:
            bot.SendTo(contact, '/微笑 你好，我是QQ机器人 - 初音ミク/Hatsune Miku，期待我们的下次相聚！')
            bot.Stop()
        elif "笑话" == cont :
            QQMsql = qqmysql.QQMsql()
            QQ_Key = QQMsql.Table('qq_keywords')
            key_count = QQ_Key.select().where(QQ_Key.key_words == cont)
            send_key = random.randint(1,len(key_count))
            print key_count[send_key].id
            data = QQ_Key.get(id=key_count[send_key].id)
            TOcontent = (" /笑哭 %s" % data.result_content)
            bot.SendTo(contact, TOcontent)
        elif "段子" == cont :
            QQMsql = qqmysql.QQMsql()
            QQ_Key = QQMsql.Table('qq_keywords')
            key_count = QQ_Key.select().where(QQ_Key.key_words == cont)
            send_key = random.randint(1,len(key_count))
            print key_count[send_key].id
            data = QQ_Key.get(id=key_count[send_key].id)
            TOcontent = (" /笑哭 %s" % data.result_content)
            bot.SendTo(contact, TOcontent)
        elif "荤段子" == cont :
            QQMsql = qqmysql.QQMsql()
            QQ_Key = QQMsql.Table('qq_keywords')
            key_count = QQ_Key.select().where(QQ_Key.key_words == cont)
            send_key = random.randint(1,len(key_count))
            print key_count[send_key].id
            data = QQ_Key.get(id=key_count[send_key].id)
            TOcontent = (" /笑哭 %s" % data.result_content)
            bot.SendTo(contact,TOcontent)




if __name__ == "__main__":
	qqbot.RunBot()