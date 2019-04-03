from bs4 import BeautifulSoup
import urllib.request
import time
import requests
import json
import re
from requests.cookies import RequestsCookieJar
import execjs

class UpdateData():
    def __init__(self,cookies,Drog_ID):

        self.get_Drog_Info(cookies,Drog_ID)
    def get_Drog_Info(self,cookies,Drog_ID):
        url = 'https://yaodian.yaofangwang.com/product/edit/'
        url += Drog_ID
        content_html = self.GetHtmlCode(cookies,url)
        #print(content_html)
        soup = BeautifulSoup(content_html, 'html.parser', from_encoding='utf-8')


        drog_id = soup.find('input',id = 'txt_AuthorizedCode')['value']  #批准文号 国药准字
        drog_commond_name = soup.find('input', id='txt_NameCN')['value']  # 通用名称
        drog_name = soup.find('input', id='txt_AliasCN')['value']  # 商品名称
        drog_type = soup.find('input', id='txt_TrocheType')['value']  # 型号
        drog_group = soup.find('input', id='txt_MillTitle')['value']  # 生产企业
        drog_num = soup.find('input', id='txt_ProductNumber')['value']  # 商品编号
        drog_standard = soup.find('input', id='txt_Standard')['value']  # 商品标准
        drog_weight = soup.find('input', id='txt_weight')['value']  # 商品重量
        drog_code = soup.find('input', id='txt_MedicineBarcode')['value']  # 条形码
        #drog_num = soup.find('input', id='ddl_ShopMedicineType')['value']  # 分类

        #jsFunc = execjs.compile('''function getValue(id){return document.getElementById(id).value;}''')

        # shop_type = execjs.compile('''document.getElementById('ddl_ShopMedicineType').value;''') # 分类
        # shop_days = execjs.compile('''document.getElementById('ddl_ScheduledDays').value;''') # 发货周期
        # shop_status = execjs.compile('''document.getElementById('ddl_Status').value;''') # 销售状态
        # shop_type = jsFunc.call('getValue','ddl_ShopMedicineType')
        # shop_days = jsFunc.call('getValue', 'ddl_ScheduledDays')
        # shop_status = jsFunc.call('getValue', 'ddl_Status')
        status_all = soup.find('select',id = 'ddl_Status')
        for status in status_all.find_all('option'):
            if 'selected' in str(status):
                shop_status = status['value']
                break
        shop_price = soup.find('input', id='txt_price')['value']  # 商城价
        #shop_price = soup.find('input', id='txt_price')['value']  # 发货周期
        shop_maxBuy = soup.find('input', id='txt_MaxBuyQty')['value']  # 最大限购
        #shop_price = soup.find('input', id='txt_price')['value']  # 销售状态
        shop_reserve = soup.find('input', id='txt_Reserve')['value']  # 商城库存

        #print(drog_id,drog_code,drog_commond_name,drog_group,drog_name,drog_num,drog_type,drog_weight)
       # print(shop_type,shop_days,shop_status)
        data = {"store_medicineid":Drog_ID,"medicine_barcode":drog_code,"authorized_code":drog_id,"namecn":drog_commond_name,"standard":drog_standard,
                "troche_type":drog_type,"aliascn":drog_name,"mill_title":drog_group,"product_number":drog_num,
                "weight":drog_weight,"reserve":shop_reserve,"max_buyqty":shop_maxBuy,"price":shop_price,"period_to":"","store_medicine_typeid":"0",
                "scheduled_days":"1","store_medicine_status":shop_status}

       # print(data_json)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
            , "Cookie": cookies}
        print(drog_commond_name)
        #_data.encode('utf-8'),
        print(url)
        r = requests.post(url,data=data,headers = headers)
        print(r.status_code)
        print(r.text)

    def GetHtmlCode(self,cookies,url):
        # 解析网页
        try:
            headers = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0")
                , ("Cookie", cookies)]
            opener = urllib.request.build_opener()
            opener.addheaders = headers
            response = opener.open(url)
            # response = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            print("error2: 网络连接超时", e)
            return None
        if response.getcode() != 200:
            print("error1: 打开网页失败，请检查您的网络！")
            return None
        content_html = response.read()
        # print(content_html.decode('utf8'))  # 解码
        return content_html



if __name__ == '__main__':
    Drog_ID = '18016379'
    cookies = 'ASP.NET_SessionId=qbg5c1zx4ramqotv505whoqm;'
    u = UpdateData(cookies,Drog_ID)
