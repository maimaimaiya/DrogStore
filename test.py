import requests
from urllib import parse
import re
def Post():
    url = "https://yaodian.yaofangwang.com/product/edit/6920054"
    postdata = "store_medicineid=6920054&medicine_barcode=6900000000000&authorized_code=%E5%9B%BD%E8%8D%AF%E5%87%86%E5%AD%97H10960036&namecn=%E7%A1%9D%E9%85%B8%E5%BC%82%E5%B1%B1%E6%A2%A8%E9%85%AF%E6%B3%A8%E5%B0%84%E6%B6%B2&standard=5ml%3A5mgx5%E6%94%AF%2F%E7%9B%92&troche_type=%E6%B3%A8%E5%B0%84%E5%89%82&aliascn=%E7%88%B1%E5%80%8D&scheduled_days=1&store_medicine_status=-999&mill_title=%E9%BD%90%E9%B2%81%E5%88%B6%E8%8D%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&product_number=xsylzql17(pal)2&weight=500&store_medicine_typeid=0&reserve=0&max_buyqty=&price=14.9&period_to="
    postdata = parse.unquote(postdata)
    print(postdata)
    postdata = '{"'+postdata.replace('=','":"') +'"}'
    postdata = postdata.replace('&','","')

    d = eval(postdata)
    print(d)
    cookie = "ASP.NET_SessionId=qbg5c1zx4ramqotv505whoqm;"
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
                , "Cookie": cookie}
    r = requests.post(url, data=d,headers = headers)
    print(r)
    print(r.text)

def GetGoodsId():
    s  = '商品编号：bknklddk4��pal��2条形码：6938270432495'
    # s = '商品编号：glbqpshxy4(pal)3条形码：6927128770025'
    com = 0.0
    if s.startswith('商品编号'):
        integer = re.findall(r"\d+\(", s)
        if (len(integer) == 0):
            integer = re.findall(r"\d+�", s)
            if(len(integer) == 0):
                integer = 0
            else:
                integer = integer[0].strip('�')
        else:
            integer = integer[0].strip('(')
        decimal = re.findall(r"\)\d+", s)
        if (len(decimal) == 0):
            decimal = re.findall(r"�\d+", s)
            if (len(decimal) == 0):
                decimal = 0
            else:
                decimal = decimal[0].strip('�')
        else:
            decimal = decimal[0].strip(')')
        com = float(str(integer) + '.' + str(decimal))
        # print(integer, " ", decimal)
        # print(com)
        # print(float(com))
    print(com)

from sys import path
from pathlib import Path
from os import makedirs
if Path(path[0] + "/data").exists() == False:
    makedirs(path[0] + "/data")