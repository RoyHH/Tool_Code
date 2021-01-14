import os
import cv2
import math
from split_xml import *
from check_jpgAndxml import *


def mkdir(path):
    # 判断路径是否存在，若不存在则创建
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)

def Col_split(img, image_pre, ext, a, row_i, sum_cols, y, split_colsize, col_dif, Outpath, i, x):
    if split_colsize * (y - math.floor(y)) < col_dif:
        for j in range(math.floor(y)):
            # b是左上角的纵轴坐标，即y1
            b = math.floor(split_colsize * (y - math.floor(y)) / 2) + split_colsize * j
            # col_j是右下角的纵轴坐标，即y2
            col_j = b + split_colsize
            part_img = img[a:row_i, b:col_j]
            newFileName = image_pre + "_split" + x + "dy" + "-" + str(i) + str(j) + ext
            print(newFileName)
            cv2.imwrite(Outpath + newFileName, part_img)

# xml文件拆分
            out_xml = 'xml_out'
            xmlFile = image_pre + ".xml"
            new_xmlFileName = image_pre + "_split" + x + "dy" + "-" + str(i) + str(j) + ".xml"
            split_xmlfile(out_xml, xmlFile, new_xmlFileName, x1=a, y1=b, x2=row_i, y2=col_j)

    else:
        for j in range(math.ceil(y)):
            b = split_colsize * j
            col_j = b + split_colsize
            if j == math.floor(y):
                b = sum_cols - split_colsize
                col_j = sum_cols

            part_img = img[a:row_i, b:col_j]
            newFileName = image_pre + "_split" + x + "-" + str(i) + str(j) + ext
            print(newFileName)
            cv2.imwrite(Outpath + newFileName, part_img)

# xml文件拆分
            out_xml = 'xml_out'
            xmlFile = image_pre + ".xml"
            new_xmlFileName = image_pre + "_split" + x + "-" + str(i) + str(j) + ".xml"
            split_xmlfile(out_xml, xmlFile, new_xmlFileName, x1=a, y1=b, x2=row_i, y2=col_j)

'''此处的split_rowsize, split_colsize根据裁剪需要修改'''
def Split_Img(img, fileName, split_rowsize=416, split_colsize=416 , row_dif=None, col_dif=None, Outpath=None):
    image_pre, ext = os.path.splitext(fileName)

    sum_rows = img.shape[0]   # the image height
    sum_cols = img.shape[1]   # the image length
    x = sum_rows / split_rowsize
    y = sum_cols / split_colsize

# 覆盖不全且未被覆盖部分可舍弃的情况
    if split_rowsize * (x - math.floor(x)) < row_dif:
        for i in range(math.floor(x)):
            # a是左上角的横轴坐标，即x1
            a = math.floor(split_rowsize * (x - math.floor(x)) / 2) + split_rowsize * i
            # row_i是右下角的横走坐标，即x2
            row_i = a + split_rowsize
            Col_split(img, image_pre, ext, a, row_i, sum_cols, y, split_colsize, col_dif, Outpath, i, "dx")
# 覆盖不全且未被覆盖部分不可舍弃，需要重叠覆盖的情况
    else:
        for i in range(math.ceil(x)):
            a = split_rowsize * i
            row_i = a + split_rowsize
            if i == math.floor(x):
                a = sum_rows - split_rowsize
                row_i = sum_rows
            Col_split(img, image_pre, ext, a, row_i, sum_cols, y, split_colsize, col_dif, Outpath, i, "")

'''InFile_do中的row_dif, col_dif根据裁剪需要修改'''
def InFile_do(Imgpath, Outpath):
    Imgpath = Imgpath + '\\'
    Outpath = Outpath + '\\'
# 有子文件
    # mkdir(Outpath)
    # for fileName in os.listdir(Imgpath):
    #     img = cv2.imread(Imgpath + fileName)
    #     img1 = img.copy()
    #     Split_Img(img1, fileName, row_dif=6, col_dif=6, Outpath=Outpath)

# 没有子文件
    for fileName in os.listdir(Imgpath):
        img = cv2.imread(Imgpath + fileName)
        img1 = img.copy()
        Split_Img(img1, fileName, row_dif=6, col_dif=6, Outpath=Outpath)


if __name__ == '__main__':
    InFile_path = "image_in"
    OutFile_path = "image_out"
    mkdir(OutFile_path)

    path_xml = 'xml_in'
    out_xml = 'xml_out'
    mkdir(out_xml)
    files_xml = sorted(os.listdir(path_xml))  # 得到文件夹下所有文件名称

    for xmlFile in files_xml:
        if not os.path.isdir(xmlFile):  # 判断是否是文件夹，不是文件夹才打开
            # print(xmlFile)
            shutil.copyfile(path_xml + "\\" + xmlFile, out_xml + "\\" + xmlFile)

    for Parent, Dir_Name, File_Name in os.walk(InFile_path):
        # 有子文件
        # for dirname in Dir_Name:
        #     Imgpath = InFile_path + '\\' + dirname
        #     Outpath = OutFile_path + '\\' + dirname
        #     InFile_do(Imgpath, Outpath)

        # 没有子文件
        InFile_do(InFile_path, OutFile_path)

    # 后处理，删除无用文件
    for xmlFile in files_xml:
        os.remove(out_xml + "\\" + xmlFile)

    # 对照jpg和xml，删除无用的jpg文件
    Check_JpgXml(jpeg_dir=OutFile_path, annot_dir=out_xml)



