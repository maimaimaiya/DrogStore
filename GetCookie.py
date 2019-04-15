from urllib import request
from urllib import error
from urllib import parse
from http.cookiejar import CookieJar
from pathlib import Path
from os import makedirs
#根据用户名和密码
def GetCookie(username,password):
    cookie = ""
    # if os.path.isfile(path[0]):
    #     path[0] = os.path.dirname(path[0])
    if Path("./data").exists() == False:
        makedirs("./data")
    try:
        # 打开文件，查看是否有对应的cookie
        # 若有，取出，并返回用户名cookie
        fp = open("./data/cookie.txt", 'r+',encoding="utf-8")
        for line in fp.readlines():
            line = line.split()
            if line[0] == username:
                cookie = line[1]
                break
        fp.close()
        #没有找到,追加cookie
        if cookie == "":
            fp = open("./data/cookie.txt", 'a+', encoding="utf-8")
            cookie = PostCookie(username,password)
            # cookie = "ASP.NET_SessionId=qbg5c1zx4ramqotv505whoqm;"
            fp.write(username + " " + cookie + "\n")
            fp.close()
    except Exception as e:
        print("no cookie:",e)
        fp = open("./data/cookie.txt", 'w+',encoding="utf-8")
        cookie = PostCookie(username,password)
        # cookie = "ASP.NET_SessionId=qbg5c1zx4ramqotv505whoqm;"
        fp.write(username + " " + cookie + "\n")
        fp.close()
    return username,cookie

#删除cookie文件
def DeleteCookie():
    fp = open("./data/cookie.txt", 'w+', encoding="utf-8")
    fp.close()

def GetHtmlCode(url,cookie):
    try:
        headers = [("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0")
                   ,("Cookie",cookie)]
        opener = request.build_opener()
        opener.addheaders = headers
        file = opener.open(url)
        content_html = file.read()
    except error.URLError as e:
        print("error2: 网络连接超时",e)
        return None
    return content_html

#若没有，post，得到cookie
def PostCookie(username,password):
    login_url = "https://reg.yaofangwang.com/login.html"
    index_url = "https://yaodian.yaofangwang.com"
    postdata = {'isRemembered': 'true',
                'LoginType': '0',
                'UserName': username,
                '__RequestVerificationToken': 'dJUkPuynv2U00CrChWF-fmGkcn2D_jZQrT22dkh3o8IK2sJz6xqtjklCeuVcO7V1GJ4iAzXEgL7Q2meGS9NpHU1Mxcpz9Wl4Fe27bdtg6qM1',
                'ImageCode': '',
                'Password': password}
    postdata = parse.urlencode(postdata).encode('utf-8')
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
              "Cookie":"__RequestVerificationToken=sTQWt8QnDlXb0618Kp-Bb3fGuzaRi7P3YK5bHIpXz856j3syyq-mJRT-tJb5dPVA9t4atK-U2DsgRmx19XtCeuPk1yi6Cap9SEeuZj07zWg1;"}
    req = request.Request(login_url, postdata, header)
    # 自动记住cookie
    cj = CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    r = opener.open(req)
    # print(cj)
    print(r.read().decode('utf-8'))
    cookie = ""
    for item in cj:
        if item.name == "ASP.NET_SessionId":
                # print("我是id：",item.value)
                cookie = "ASP.NET_SessionId=" + item.value+";"
                break
        else:
            print(item)
    # get请求一次首页
    GetHtmlCode(index_url,cookie)
    return cookie


if __name__ == '__main__':
    username = "刘茂东3"
    password = "1q2w3e4r"
    # cookie = "ASP.NET_SessionId=qbg5c1zx4ramqotv505whoqm;"
    goods_url = "https://yaodian.yaofangwang.com/product/list/"
    # PostCookie(username,password)
    username,cookie = GetCookie(username,password)
    print(username,cookie)
#保存对应的账号和cookie到文件

#返回数据

###更新cookie
#取出文件所有数据
#更新对应用户的cookie