from urllib import request
import urllib
from bs4 import BeautifulSoup as BS
import re
import time
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
import pandas

#得到网页源代码
#参数：网址
#返回：网页源代码
def GetHtmlCode(url,cookie):
    # 解析网页
    try:
        print(url)
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        #     , "Cookie": cookie}
        headers = [("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0")
                   ,("Cookie",cookie)]
        opener = urllib.request.build_opener()
        opener.addheaders = headers
        file = opener.open(url)
        content_html = file.read()
        # print(content_html)
        # response = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print("error2: 网络连接超时",e)
        return None
    # except Exception as e:
    #     print(e)
    #     return None
    # if response.getcode() != 200:
    #     print("error1: 打开网页失败，请检查您的网络！")
    #     return None
    # content_html = file.read()
    # print(content_html.decode('utf8'))  # 解码
    return content_html

#得到总页数
#soup
#返回：页数(int)
def GetPageNum(soup):
    page_info = soup.find('div', class_="info")
    num = re.findall(r"条，共 (.+?) 页", str(page_info))
    return int(num[0])

#得到商品编号价格
def GetIdPrice(s):
    # s = '商品编号：glbqpshxy4(pal)3条形码：6927128770025'
    com = 0.0
    if s.startswith('商品编号'):
        integer = re.findall(r"\d+\(", s)
        if (len(integer) == 0):
            integer = 0

        else:
            integer = integer[0].strip('(')
        decimal = re.findall(r"\)\d+", s)
        if (len(decimal) == 0):
            decimal = 0
        else:
            decimal = decimal[0].strip(')')
        com = float(str(integer) + '.' + str(decimal))
        # print(integer, " ", decimal)
        # print(com)
        # print(float(com))
    return com

#获取商品编号
#goods_num,goods_id_arr
#商品数，商品编号数组
def GetGoodsId(soup):
    # 商品编号
    goods_id = soup.find_all('tr', class_="bg-grey-cararra")
    # 商品数
    goods_num = len(goods_id)
    # print("商品数：", goods_num)
    # 商品编号数组
    goods_id_arr = []
    goods_id_price_arr = []
    for i in range(goods_num):
        goods_id_temp = goods_id[i].find('td', colspan="7").get_text()
        goods_id_temp = goods_id_temp.replace("\n", "")
        # print(i, '：', goods_id_temp)
        goods_id_arr.append(goods_id_temp)
        #正则表达式获取价格
        goods_id_price = GetIdPrice(goods_id_temp)
        goods_id_price_arr.append(goods_id_price)
    return goods_num,goods_id_arr,goods_id_price_arr

#写文件
def WriteXls(sheet, url,quasi, spec, id, price,state,id_price,row_count):
    # write(行，列，值)
    # print(name,total,sales_max)
    # style = xlwt.XFStyle()
    # style.num_format_str = '0.00%'
    sheet.write(row_count, 0, url)
    sheet.write(row_count, 1, quasi)
    sheet.write(row_count, 2, spec)
    sheet.write(row_count, 3, id)
    sheet.write(row_count, 4, price)
    sheet.write(row_count, 5, state)
    sheet.write(row_count, 6, id_price)


###获取商品数据
#cookie
#username 用户名
def GetData(cookie,username):
    pageNum = 1
    url = "https://yaodian.yaofangwang.com/product/list/?page=" + str(pageNum)
    html_content = GetHtmlCode(url, cookie)
    soup = BS(html_content, 'html.parser', from_encoding='utf-8')
    # print(soup)
    #获取总页数
    page_num = GetPageNum(soup)
    #存excel数据
    row_count = 0
    save_file = xlwt.Workbook()
    sheet1 = save_file.add_sheet('药房网', cell_overwrite_ok=True)
    WriteXls(sheet1,"商品url", "国药准字", "规格", "商品编号","商城价格","发布状态","编号价格",row_count)
    save_file.save('data/' + username + '.xls')
    #循环每一页得到数据
    for index in range(1, page_num+1):#page_num+1
        start_time = time.time()
        #获取每一页数据
        if index != 1:
            url = "https://yaodian.yaofangwang.com/product/list/?page=" + str(index)
            html_content = GetHtmlCode(url, cookie)
            soup = BS(html_content, 'html.parser', from_encoding='utf-8')
        #商品数，商品编号
        goods_num, goods_id_arr,goods_id_price_arr = GetGoodsId(soup)
        #
        soup_all = soup.find_all('tr')
        # print("总数：",len(soup_all))
        goods_url_arr = []
        goods_quasi_arr = []
        goods_spec_arr = []
        goods_price_arr = []
        goods_state_arr = []
        #数据存excel表
        for i in range(1,goods_num+1):
            i = i*2
            # print(soup_all[i])
            goods_all = soup_all[i].find_all('td')
            # print("goods_all",len(goods_all))
            #链接
            goods_url = goods_all[6].find('a')['href']
            goods_single = goods_all[1].find_all('div', class_="text-left")
            #准字
            goods_quasi = goods_single[1].get_text().strip()
            #规格
            goods_spec = goods_single[2].get_text().strip()
            # print(goods_url)
            # print(goods_quasi)
            # print(goods_spec)
            goods_url_arr.append(goods_url)
            goods_quasi_arr.append(goods_quasi)
            goods_spec_arr.append(goods_spec)
            #商城价格
            goods_price = goods_all[2].find('span').get_text()
            goods_price = float(goods_price.strip('¥'))
            # print(goods_price)
            goods_price_arr.append(goods_price)
            #状态
            goods_state = goods_all[4].find('div').get_text().strip()
            # print(goods_state)
            goods_state_arr.append(goods_state)
        #存一页数据表中
        for i in range(goods_num):
            row_count += 1
            # rexcel = open_workbook('data/' + username + '.xls')  # 用wlrd提供的方法读取一个excel文件
            # excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
            # table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
            WriteXls(sheet1, goods_url_arr[i], goods_quasi_arr[i], goods_spec_arr[i], goods_id_arr[i],
                     goods_price_arr[i], goods_state_arr[i], goods_id_price_arr[i], row_count)
            # excel.save('data/' + username + '.xls')  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
        if(index % 50 == 0 or index == page_num + 1):
            save_file.save('data/' + username + '.xls')
        print("第 ",index, " 页")
        # time.sleep(3)
        end_time = time.time()
        print("时间：",end_time-start_time)
    # print(soup)

if __name__ == '__main__':
    cookie = "ASP.NET_SessionId=qbg5c1zx4ramqotv505whoqm;"
    username = "刘茂东3"
    GetData(cookie,username)
