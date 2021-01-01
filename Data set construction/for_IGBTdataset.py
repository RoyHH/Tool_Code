import os
import cv2
import math
from shutil import copyfile
from openpyxl import load_workbook
import xlwings as xw
import numpy as np

def mkdir(path):
    # 判断路径是否存在，若不存在则创建
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)

'''InFile_do中的row_dif, col_dif根据裁剪需要修改'''
def PIC_do(InFile_path, OutFile_path):
    for Parent, Dir_Name, File_Name in os.walk(InFile_path):
        for filename in File_Name:
            print("filename: ", filename)
            print("path: ", Parent)
            img = cv2.imread(Parent + '\\' + filename)
            img1 = img.copy()
            cv2.imwrite(OutFile_path + '\\' + filename, img1)

def File_do(InFile_path, OutFile_path):
    for Parent, Dir_Name, File_Name in os.walk(InFile_path):
        for filename in File_Name:
            print("filename: ", filename)
            print("path: ", Parent)
            copyfile(Parent + '\\' + filename, OutFile_path + '\\' + filename)

def DEL_do(pic_path, excel_path):
    app = xw.App(visible=True, add_book=False)
    excel_open = app.books.open(excel_path)
    # excel_open = xw.Book(excel_path)
    print(excel_open)
    excel_open.activate()
    # print(excel_open.name)
    excel_name, ext = os.path.splitext(excel_open.name)
    # print(excel_name)
    Sheet = excel_open.sheets['异常记录']
    print(Sheet)
    Sheet.activate()
    wrong_list = []
    for i in range (2,29):
        wrong_list.append(Sheet.range('c' + str(i)).value)
        print(wrong_list)

    excel_open.close()  # 关闭工作簿(程序不能编辑了)----显示的文件不关闭
    app.quit()  # 退出应用---显示的文件也关闭

    for j in range(len(wrong_list)):
        print(pic_path + '/' +wrong_list[j] + ".jpg")
        if os.path.exists(pic_path + '/' +wrong_list[j] + ".jpg"):
            os.remove(pic_path + '/' +wrong_list[j] + ".jpg")
            print("删除成功")
        else:
            print("%s 中没有 %s 文件" %(pic_path, wrong_list[j]))

def main():
    InFile_path = "data/New Data-jpg/IGBT_PIC"
    OutFile_path = "data/New Data-jpg/IGBT_Img"
    mkdir(OutFile_path)

    InLabel_path = "data/New Data-jpg/Labels"
    OutLabel_path = "data/New Data-jpg/IGBT_Labels"
    mkdir(OutLabel_path)

# 整理图片文件
    PIC_do(InFile_path, OutFile_path)

# 整理标签文件
    File_do(InLabel_path, OutLabel_path)

    # for Parent, Dir_Name, File_Name in os.walk(InFile_path):
    #     for filename in File_Name:
    #         print("filename: ", filename)
    #         print("path: ", Parent)
    #         img = cv2.imread(Parent + '\\' + filename)
    #         img1 = img.copy()
    #         cv2.imwrite(OutFile_path + '\\' + filename, img1)

# 处理图片与标签不对应的文件，将其删除，使得保持图片与标签一一对应
    excel_path = "data/New Data-jpg/数据采集记录.xlsx"
    DEL_do(OutFile_path, excel_path)

if __name__ == '__main__':
   main()