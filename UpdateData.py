# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from urllib import error
from urllib.request import build_opener
from requests import post

def Updata_Drog_Info(cookies,url,shop_reserve=-10,drog_num=-10,shop_status=-10,shop_price=-10): # 库存，药品编号，上下架,商城价
    # url = 'https://yaodian.yaofangwang.com/product/edit/'
    # url += Drog_ID
    Drog_ID = url.replace("https://yaodian.yaofangwang.com/product/edit/","")
    # 根据ID获取网页源码
    content_html = GetHtmlCode(cookies,url)
    #print(content_html)
    soup = BeautifulSoup(content_html, 'html.parser', from_encoding='utf-8')


    drog_id = soup.find('input',id = 'txt_AuthorizedCode')['value']  #批准文号 国药准字
    drog_commond_name = soup.find('input', id='txt_NameCN')['value']  # 通用名称
    drog_name = soup.find('input', id='txt_AliasCN')['value']  # 商品名称
    drog_type = soup.find('input', id='txt_TrocheType')['value']  # 型号
    drog_group = soup.find('input', id='txt_MillTitle')['value']  # 生产企业
    if drog_num==-10:
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
    if shop_status == -10:
        for status in status_all.find_all('option'):
            if 'selected' in str(status):
                shop_status = status['value']
                break
    else:
        status_dict={}
        status_dict['上架'] = 1
        status_dict['发布'] = 1
        status_dict['热销'] = 2
        status_dict['促销'] = 3
        status_dict['新品'] = 4
        status_dict['推荐'] = 5
        status_dict['特价'] = 6
        status_dict['下架'] = -999
        shop_status = status_dict[shop_status]

    if shop_price == -10:
        shop_price = soup.find('input', id='txt_price')['value']  # 商城价
    #shop_price = soup.find('input', id='txt_price')['value']  # 发货周期
    shop_maxBuy = soup.find('input', id='txt_MaxBuyQty')['value']  # 最大限购
    #shop_price = soup.find('input', id='txt_price')['value']  # 销售状态
    if shop_reserve == -10:
        shop_reserve = soup.find('input', id='txt_Reserve')['value']  # 商城库存

    #print(drog_id,drog_code,drog_commond_name,drog_group,drog_name,drog_num,drog_type,drog_weight)
   # print(shop_type,shop_days,shop_status)
    # 数据字典
    #"store_medicineid":Drog_ID,
    data = {"store_medicineid":Drog_ID,"medicine_barcode":drog_code,"authorized_code":drog_id,"namecn":drog_commond_name,"standard":drog_standard,
            "troche_type":drog_type,"aliascn":drog_name,"mill_title":drog_group,"product_number":drog_num,
            "weight":drog_weight,"reserve":shop_reserve,"max_buyqty":shop_maxBuy,"price":shop_price,"period_to":"","store_medicine_typeid":"0",
            "scheduled_days":"1","store_medicine_status":str(shop_status)}

   # print(data_json)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        , "Cookie": cookies}
    try:
        print(drog_commond_name)
    except Exception as e:
        print(e)
        
    #_data.encode('utf-8'),
    print(url)
    r = post(url,data=data,headers = headers)
    print(r.status_code)
    # print(r.text)

def GetHtmlCode(cookies,url):
    # 解析网页
    try:
        headers = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0")
            , ("Cookie", cookies)]
        opener = build_opener()
        opener.addheaders = headers
        response = opener.open(url)
        # response = urllib.request.urlopen(url)
    except error.URLError as e:
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
    cookie = 'ASP.NET_SessionId=5y243edgijtoprlzhqbmnujp;'
    cookies = 'ASP.NET_SessionId=qbg5c1zx4ramqotv505whoqm;'
    try:
        Updata_Drog_Info(cookie,"https://yaodian.yaofangwang.com/product/edit/5698539")
    except Exception as e:
        print(e)
    #time.sleep(1000)
    # u = UpdateData(cookies,Drog_ID)
