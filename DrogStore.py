import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

# 先来个窗口
class window(QWidget):

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.box = QVBoxLayout(self)  # 创建一个垂直布局来放控件
        #self.btn_get = QPushButton('点击获取cookies')  # 创建一个按钮涌来了点击获取cookie
        #self.btn_get.clicked.connect(self.get_cookie)  # 绑定按钮点击事件

        self.web = MyWebEngineView()  # 创建浏览器组件对象
        self.web.resize(800, 600)  # 设置大小
        self.web.load(QUrl("https://reg.yaofangwang.com/login.html"))  # 打开百度页面来测试
#        self.box.addWidget(self.btn_get)  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.web)  # 再放浏览器
        self.web.show()  # 最后让页面显示出来
        self.web.loadFinished.connect(self.get_cookie)



    def get_cookie(self):
        #https://yaodian.yaofangwang.com/
        print(self.web.url())
        if self.web.url()!= QUrl("https://yaodian.yaofangwang.com/"):
            return
        print('登陆成功')
        user_name,cookie = self.web.get_cookie()
        print('获取到用户名: ', user_name)
        print('获取到cookie: ', cookie)
        sys.exit(app.exec_())


# 创建自己的浏览器控件，继承自QWebEngineView
class MyWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(MyWebEngineView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}  # 存放cookie字典

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value  # 将cookie保存到字典里

    # 获取cookie
    def get_cookie(self):
        cookie_str = 'ASP.NET_SessionId='
        user_name = self.cookies['logined_username']
        cookie_str += self.cookies['ASP.NET_SessionId']
        # for key, value in self.cookies.items():  # 遍历字典
        #     cookie_str += (key + '=' + value + ';')  # 将键值对拿出来拼接一下
        return user_name,cookie_str  # 返回拼接好的字符串


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = window()
    w.show()
    sys.exit(app.exec_())
