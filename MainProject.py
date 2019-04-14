import wx
import wx.xrc
import wx.grid

from requests import get
from threading import Thread
from pandas import DataFrame
from pandas import read_excel
from wx.lib.pubsub import pub
import GetData as GD
import GetUrl as GU
import GetCookie as GC
import os
class GetDataThread(Thread):
    def __init__(self):
        #线程实例化时立即启动
        Thread.__init__(self)
        #主线程关闭
        self.setDaemon(True)
        self.start()
    def run(self):
        #线程执行的代码
        global cookie
        global username
        GD.GetData(cookie, username)
        wx.CallAfter(pub.sendMessage, "update", msg="getdata")

class UpdateThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.start()
    def run(self):
        #更新信息- 合并数据、打开对应文件、修改对应数据
        GU.MergeData(username,cookie, open_file_path)
        # GetOnlineData("刘茂东3", 1.1)
        wx.CallAfter(pub.sendMessage, "update", msg="update")

class SelectThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.start()
    def run(self):
        global df
        GU.GetOnlineData(username, id_multiple)
        wx.CallAfter(pub.sendMessage, "update", msg="select")

class PriceThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.start()
    def run(self):
        global select_list
        GU.UpdatePrice(username,cookie, multiple,select_list)
        wx.CallAfter(pub.sendMessage, "update", msg="price")

class CookieThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.start()
    def run(self):
        global username
        global cookie
        if isupdate == 0:
            username,cookie = GC.GetCookie(username,password)
            wx.CallAfter(pub.sendMessage, "update", msg="cookie")
        else:
            GC.DeleteCookie()
            wx.CallAfter(pub.sendMessage, "update", msg="updatecookie")

###########################################################################
## Class Drog
###########################################################################

class Drog(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"药房网商品修改 V1.0", pos=wx.DefaultPosition,
                          size=wx.Size(580, 450), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.bSizer1 = wx.BoxSizer(wx.VERTICAL)
        ###登录
        self.bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"用户名:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        self.bSizer4.Add(self.m_staticText3, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl41 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer4.Add(self.m_textCtrl41, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button6 = wx.Button(self, wx.ID_ANY, u"立即登录", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer4.Add(self.m_button6, 0, wx.ALL, 5)

        self.bSizer1.Add(self.bSizer4, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"密   码:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        self.bSizer5.Add(self.m_staticText4, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer5.Add(self.m_textCtrl5, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button7 = wx.Button(self, wx.ID_ANY, u"更新Cookie", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer5.Add(self.m_button7, 0, wx.ALL, 5)

        self.bSizer1.Add(self.bSizer5, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL, 5)
        ###

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer2.SetMinSize(wx.Size(500, 30))
        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, 30), 0)
        bSizer2.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"选择文件", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_button1, 0, wx.ALL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"获取数据", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_button2, 0, wx.ALL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"修改信息", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_button3, 0, wx.ALL, 5)

        self.bSizer1.Add(bSizer2, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL, 1)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, u"1.1", wx.DefaultPosition, wx.Size(32, -1), 0)
        bSizer3.Add(self.m_textCtrl2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"*编号价格>商品价格 修改为", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer3.Add(self.m_staticText1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, u"1.5", wx.DefaultPosition, wx.Size(32, -1), 0)
        bSizer3.Add(self.m_textCtrl3, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"*编号价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer3.Add(self.m_staticText2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"筛选商品", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.m_button4, 0, wx.ALL, 5)

        self.m_button5 = wx.Button(self, wx.ID_ANY, u"修改价格", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.m_button5, 0, wx.ALL, 5)

        self.bSizer1.Add(bSizer3, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL, 1)

        self.m_grid1 = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid1.CreateGrid(14, 5)
        self.m_grid1.EnableEditing(True)
        self.m_grid1.EnableGridLines(True)
        self.m_grid1.EnableDragGridSize(False)
        self.m_grid1.SetMargins(0, 0)

        # Columns
        self.m_grid1.SetColSize(0, 110)
        self.m_grid1.SetColSize(1, 110)
        self.m_grid1.SetColSize(2, 110)
        self.m_grid1.SetColSize(3, 110)
        self.m_grid1.SetColSize(4, 50)
        self.m_grid1.EnableDragColMove(False)
        self.m_grid1.EnableDragColSize(True)
        self.m_grid1.SetColLabelSize(25)
        self.m_grid1.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.m_grid1.EnableDragRowSize(True)
        self.m_grid1.SetRowLabelSize(25)
        self.m_grid1.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        self.m_grid1.SetColLabelValue(0, "全选 商品编号")
        self.m_grid1.SetColLabelValue(1, "名称")
        self.m_grid1.SetColLabelValue(2, "厂家")
        self.m_grid1.SetColLabelValue(3, "规格")
        self.m_grid1.SetColLabelValue(4, "商城价格")

        # Label Appearance

        # Cell Defaults
        self.m_grid1.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        self.bSizer1.Add(self.m_grid1, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)


        self.SetSizer(self.bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        #绑定点击按钮的事件
        #选择文件
        self.m_button1.Bind(wx.EVT_BUTTON, self.OnOpenFile)
        #获取数据
        self.m_button2.Bind(wx.EVT_BUTTON, self.GetDrogData)
        #修改信息
        self.m_button3.Bind(wx.EVT_BUTTON, self.Update)
        self.m_button4.Bind(wx.EVT_BUTTON, self.SelectDrog)
        self.m_button5.Bind(wx.EVT_BUTTON, self.UpdatePrice)
        self.m_button6.Bind(wx.EVT_BUTTON, self.Login)
        self.m_button7.Bind(wx.EVT_BUTTON, self.UpdateCookie)
        pub.subscribe(self.updateDisplay, "update")

        html_info = get(URL_MMP)
        if html_info.status_code != 200:
            wx.MessageBox("软件出现错误，请检查您的网络 或 联系开发人员！！！", "you are wrong", wx.OK | wx.YES_DEFAULT)
            self.Destroy()

    def __del__(self):
        pass

    #更新消息
    def updateDisplay(self, msg):
        t = msg
        if t == "getdata":
            self.m_button2.Enable()
            wx.MessageBox("已经成功获取商城所有数据", "完成消息", wx.OK | wx.YES_DEFAULT)
        elif t == "update":
            self.m_button3.Enable()
            wx.MessageBox("已经成功修改商城对应数据", "完成消息", wx.OK | wx.YES_DEFAULT)
        elif t == "select":
            self.m_button4.Enable()
            #显示数据
            df = DataFrame(read_excel("./data/" + username + "_price.xls"))
            rows = int(df.shape[0])
            # self.m_grid1.CreateGrid(rows,5)
            #删除行
            self.m_grid1.DeleteRows(numRows=self.m_grid1.GetNumberRows())
            self.m_grid1.AppendRows(rows)
            # print(df)
            for i in range(rows):
                single_data = df.loc[i]
                self.m_grid1.SetCellValue(i,0,single_data["商品编号"])
                self.m_grid1.SetCellValue(i, 1, single_data["名称1"])
                self.m_grid1.SetCellValue(i, 2, single_data["厂家1"])
                self.m_grid1.SetCellValue(i, 3, str(single_data["规格"]))
                self.m_grid1.SetCellValue(i, 4, str(single_data["商城价格"]))
            wx.MessageBox("已经成功筛选对应数据", "完成消息", wx.OK | wx.YES_DEFAULT)
        elif t == "price":
            self.m_button5.Enable()
            wx.MessageBox("已经成功修改价格", "完成消息", wx.OK | wx.YES_DEFAULT)
        elif t == "cookie":
            # 隐藏登录按钮
            self.bSizer1.Hide(self.bSizer5)
            self.bSizer1.Hide(self.bSizer4)
            self.SetSizer(self.bSizer1)
            self.Layout()
            print("登录完成")
        elif t == "updatecookie":
            global isupdate
            isupdate = 0
            wx.MessageBox("Cookie更新完成，请重新登录", "完成消息", wx.OK | wx.YES_DEFAULT)

    def UpdateCookie(self,event):
        global isupdate
        isupdate = 1
        CookieThread()

    #立即登录
    def Login(self,event):
        #获取用户名和cookie
        if self.m_textCtrl41.GetValue() == "" or self.m_textCtrl5.GetValue() == "":
            wx.MessageBox("请填写用户名和密码", "提示消息", wx.OK | wx.YES_DEFAULT)
            return
        global username
        global password
        username = self.m_textCtrl41.GetValue()
        password = self.m_textCtrl5.GetValue()
        #开启线程获取cookie
        CookieThread()

    def UpdatePrice(self,event):
        if self.m_textCtrl2.GetValue() == "":
            wx.MessageBox("请填写商品价格的倍数", "提示消息", wx.OK | wx.YES_DEFAULT)
        elif self.m_textCtrl3.GetValue() == "":
            wx.MessageBox("请填写要修改的倍数", "提示消息", wx.OK | wx.YES_DEFAULT)
        elif self.m_grid1.GetCellValue(0,0) == "":
            wx.MessageBox("请先点击筛选商品", "提示消息", wx.OK | wx.YES_DEFAULT)
        else:
            global id_multiple
            global multiple
            id_multiple = float(self.m_textCtrl2.GetValue())
            multiple = float(self.m_textCtrl3.GetValue())
            #修改价格
            #获取选定的行
            global select_list
            select_list = []
            rows = self.m_grid1.GetNumberRows()
            for i in range(rows):
                if self.m_grid1.IsInSelection(i,0):
                    select_list.append(i)
            # print(select_list)
            PriceThread()
            event.GetEventObject().Disable()

    def SelectDrog(self,event):
        if self.m_button2.IsEnabled() == False:
            wx.MessageBox("请先等待数据获取完成，再进行操作", "提示消息", wx.OK | wx.YES_DEFAULT)
            return
        if self.m_textCtrl2.GetValue() == "":
            wx.MessageBox("请填写商品价格的倍数", "提示消息", wx.OK | wx.YES_DEFAULT)
        elif self.m_textCtrl3.GetValue() == "":
            wx.MessageBox("请填写要修改的倍数", "提示消息", wx.OK | wx.YES_DEFAULT)
        # self.m_textCtrl1.write(self.dlg.GetPath())
        else:
            # 筛选商品
            global id_multiple
            global multiple
            id_multiple = float(self.m_textCtrl2.GetValue())
            multiple = float(self.m_textCtrl3.GetValue())
            SelectThread()
            event.GetEventObject().Disable()

    def Update(self, event):
        if self.m_button2.IsEnabled() == False:
            wx.MessageBox("请先等待数据获取完成，再进行操作", "提示消息", wx.OK | wx.YES_DEFAULT)
            return
        if open_file_path == "":
            wx.MessageBox("请先选择要更新的文件", "提示消息", wx.OK | wx.YES_DEFAULT)
        else:
            UpdateThread()
            event.GetEventObject().Disable()

    # 获取数据
    def GetDrogData(self, event):
        GetDataThread()
        event.GetEventObject().Disable()
    #打开文件
    def OnOpenFile(self, event):
        # 根据单选的索引执行
        #设置工作目录
        wd = os.getcwd()
        filesFilter = "Xls Files (*.xls)|*.xls|" "All files (*.*)|*.*"
        # 选择文件对话框，设置选择的文件必须为xls格式
        self.dlg = wx.FileDialog(self, message=u"选择文件", style=wx.FD_OPEN | wx.FD_CHANGE_DIR,
                                 wildcard=filesFilter)
        # 如果确定了选择的文件，将文件路径写到text1控件
        if self.dlg.ShowModal() == wx.ID_OK:
            global open_file_path
            open_file_path = self.dlg.GetPath()
            self.m_textCtrl1.Clear()
            self.m_textCtrl1.write(self.dlg.GetPath())
        os.chdir(wd)

def Run(username1,cookie1):
    open_file_path = ""
    username = username1
    cookie = cookie1
    id_multiple = 1.1
    multiple = 1.5
    select_list = []

    URL_MMP = 'http://demo.xx2018.cn/19331%E8%8D%AF%E6%88%BF%E9%80%9A%E5%95%86%E5%93%81%E4%BF%AE%E6%94%B9.txt'
    app = wx.App(False)
    frame = Drog(None)
    # 根据自己的类名来生成实例
    frame.Show(True)
    # start the applications
    app.MainLoop()

if __name__ == '__main__':
    open_file_path = ""
    # cookie = "ASP.NET_SessionId=qbg5c1zx4ramqotv505whoqm;"
    # username = "刘茂东3"
    username = ""
    password = ""
    cookie = ""
    isupdate = 0
    id_multiple = 1.1
    multiple = 1.5
    select_list = []
    URL_MMP = 'http://demo.xx2018.cn/19331%E8%8D%AF%E6%88%BF%E9%80%9A%E5%95%86%E5%93%81%E4%BF%AE%E6%94%B9.txt'
    # GetData(cookie, username)
    app = wx.App(False)
    frame = Drog(None)
    # 根据自己的类名来生成实例
    frame.Show(True)
    # start the applications
    app.MainLoop()