# -*- coding:UTF-8 -*-

'''
用于处理日常行为数据。
根据下载下来的数据文件，日常行为的数据文件解析和提取与跌到数据文件处理存在不同之处。

需要实现的功能：
1.通过调用data_graph里面的adl_line_chart方法查看需要截取的数据范围，
获取需要截取的数据。
2.日常行为数据传感器采集频率为200hz，而跌倒数据采集频率为100hz，
所以需要进步提取数据，并将提取的数据保存至新的csv文件中。

3.向用户询问，一份csv文件需要提取几份数据。通过调用data_graph中
adl_chart_for_extract_multi_data方法来获取需要截取的每段数据begin值，
通过begin来进行数据保存。
'''
import os
import pandas as pd
import numpy as np
import data_graph as dp
# import matplotlib.pyplot as plt


ADL_DATA_SAVE_FILE = "../data/raw_data/ADL/WAL/WALK_data.csv"
INDEX_FILE = '../data/raw_data/ADL/JUM/indexfile.csv'
path = '/home/tony/fall_research/fall_data/MobiAct_Dataset_v2.0/Annotated Data/JUM'

Label = {'STD':1,'WAL':2,'JOG':3,'JUM':4,'STU':5,'STN':6,'SCH':7,'SIT':8,'CHU':9,'CSI':10,'CSO':11,'LYI':12,'FOL':0,'FKL':0,'BSC':0,'SDL':0}

def extract_data(annotated_data,begin,end,label,save_data_file=ADL_DATA_SAVE_FILE):
    """
    提取数据，根据参数，截取定长数据来存储到new_data_file中.
    截取的数据长度=end+1-begin
    :param annotated_data: 数据
    :param begin: 数据的起始段
    :param end: 数据的终止段
    :param label: 数据分类类型
    :param save_data_file: 攫取的数据存储文件
    :return: 返回存储好的文件
    """
    if (end-begin)!=400:
        print('数据截取长度不为400份')
        return 'error'

    acc_extract_data = annotated_data.iloc[begin:end:2, 6:9].values
    gyro_extract_data = annotated_data.iloc[begin:end:2, 3:6].values

    with open(save_data_file, "a+") as data_file:
        data_file.seek(0,os.SEEK_SET)
        if data_file.read()=="":
            data_file.write("label")
            for i in range(1200):
                data_file.write(","+str(i+1))
            data_file.write("\n")

        data_file.seek(0, os.SEEK_END)
        # 在数据每一行中，第一位代表数据标签。0代表跌倒数据,非0代表日常活动数据
        data_file.write(str(Label[label]))

        for data in acc_extract_data:
            line_data = ","+str(data[0])+","+str(data[1])+","+str(data[2])
            data_file.write(line_data)

        for data in gyro_extract_data:
            line_data = ","+str(data[0])+","+str(data[1])+","+str(data[2])
            data_file.write(line_data)
        # 传感器有加速度和陀螺仪，所以提取完陀螺仪后自动完成换行，方便提取新的一行数据
        data_file.write("\n")
    # print("从",annotated_file,"文件中提取",str((end-begin)/2),"份数据。\n已保存至",save_data_file)
    #datafile = pd.read_csv(save_data_file)
    # position值表示save_data_file中excel存储数据位置的标号
    #position = len(datafile.label)+1
    #save_extracted_file(annotated_file,position)

    return None

def save_extracted_file(save_data_file,position):
    with open(INDEX_FILE, "a+") as index_file:
        index_file.seek(0,os.SEEK_SET)
        if index_file.read()=="":
            index_file.write("Name")
            index_file.write(","+"position")
            index_file.write("\n")
        index_file.seek(0,os.SEEK_END)
        index_file_data = save_data_file+","+str(position)
        index_file.write(index_file_data)
        index_file.write("\n")
    # print("已将文件处理完成加入索引！")


def find_and_extract():
    '''
    循环读取文件,提取数据
    :return:
    '''

    data = pd.read_csv('/home/tony/fall_research/fall_data/SisFall_dataset/SisFall_dataset/SA01/D02_SA01_R01.csv')
    # 每个文件截取范围
    extract_row = np.random.randint(500, 9000, 1060)
    for i in range(1060):
        print('提取行号为：',extract_row[i])
        extract_data(data, int(extract_row[i]), int(extract_row[i]) + 400, 'WAL')


def main():
    find_and_extract()

    # data_file = pd.read_csv('../data/raw_data/ADL/WAL/indexfile.csv',index_col=False)
    # print(data_file.Name[3])
    # print(len(data_file.Name))


if __name__ == "__main__":
    main()