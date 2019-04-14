#file_path

from pandas import DataFrame
from pandas import read_excel
from pandas import merge
import xlrd
import UpdateData as UD

#合并爬取数据，与上传数据
def MergeData(username,cookie,update_path):
    file_path = "./data/"+username+".xls"
    df = DataFrame(read_excel(file_path))
    df_update = DataFrame(read_excel(update_path))
    #合并两个表
    df_inner = merge(df, df_update, how='inner')
    # print(df_inner)
    #保存到本地
    df_inner.to_excel("./data/"+username+"_merge.xls", index=False)

    #调用接口修改
    cow_num  = df_inner.shape[0]
    # 一行行读数据
    for index in range(cow_num):
        #按行取数据
        single_data = df_inner.loc[index]
        # 调用接口post修改数据
        UD.Updata_Drog_Info(cookie,single_data["商品url"],single_data["库存"]
                            ,single_data["药品编码"],single_data["上下架"])
        # time.sleep(1000)

#获取在线商品
#条件 商城价格 < 编号价格*倍数 修改 编号价格*倍数
#用户名，编号价格倍数，修改后倍数
def GetOnlineData(username,id_multiple):
    #在线
    file_path ="./data/" + username + ".xls"
    df = DataFrame(read_excel(file_path))
    #url、商城价格、编号价格*倍数、修改后价格
    #查找在线商品
    df = df.loc[df['发布状态'] == '发布']
    df = df.loc[df["商城价格"] < df["编号价格"] * id_multiple]
    #查找 商城价格 < 编号价格*倍数
    # print(df)
    df.to_excel("./data/" + username + "_price.xls", index=False)
    print("筛选商品")
    # return df

#修改对应价格到网站
def UpdatePrice(username,cookie,multiple,select_list):
    file_path = "./data/" + username + "_price.xls"
    df = DataFrame(read_excel(file_path))
    cow_num = df.shape[0]
    for index in select_list:
        single_data = df.loc[index]
        single_data["商品url"]
        #调用接口修改价格
        UD.Updata_Drog_Info(cookie, single_data["商品url"],shop_price=single_data["编号价格"] * multiple)
    print("修改价格")


if __name__ == '__main__':
    update_path = "data/下架1.xls"
    MergeData("刘茂东3",update_path)
    GetOnlineData("刘茂东3",1.1)











