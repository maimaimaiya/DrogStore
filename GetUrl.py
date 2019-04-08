#file_path

import xlrd
import pandas as pd
import time

#获取在售中价格数据

#合并爬取数据，与上传数据
def MergeData(username,update_path):
    file_path = "data/"+username+".xls"
    df = pd.DataFrame(pd.read_excel(file_path))
    df_update = pd.DataFrame(pd.read_excel(update_path))
    #合并两个表
    df_inner = pd.merge(df, df_update, how='inner')
    # print(df_inner)
    #保存到本地
    df_inner.to_excel("data/"+username+"_merge.xls", index=False)

    #修改
    cow_num  = df_inner.shape[0]
    # 一行行读数据
    for index in range(cow_num):
        #按行取数据
        single_data = df_inner.loc[index]
        # 调用接口post修改数据
        #
        #
        #
        print(single_data["商品url"])
        single_data["库存"]
        single_data["药品编号"]
        single_data["上下架"]
        time.sleep(1000)

#获取在线商品
#条件 商城价格 < 编号价格*倍数 修改 编号价格*倍数
#用户名，编号价格倍数，修改后倍数
def GetOnlineData(username,id_multiple):
    #在线
    file_path = "data/" + username + ".xls"
    df = pd.DataFrame(pd.read_excel(file_path))
    #url、商城价格、编号价格*倍数、修改后价格
    #查找在线商品
    df = df.loc[df['发布状态'] == '发布']
    df = df.loc[df["商城价格"] < df["编号价格"] * id_multiple]
    #查找 商城价格 < 编号价格*倍数
    print(df)
    df.to_excel("data/" + username + "_price.xls", index=False)

if __name__ == '__main__':
    update_path = "data/下架1.xls"
    # MergeData("刘茂东3",update_path)
    GetOnlineData("刘茂东3",1.1)










