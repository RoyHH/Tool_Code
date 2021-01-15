import os
import cv2
import math
from split_xml import *
import glob

def mkdir(path):
    # 判断路径是否存在，若不存在则创建
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)

def Col_split(img, image_pre, ext, a, row_i, sum_cols, Num_vertical, split_colsize, col_dif, Outpath, i, x):
    if split_colsize * (Num_vertical - math.floor(Num_vertical)) - 0.2 * split_colsize < col_dif:
        for j in range(math.floor(Num_vertical)):
            # b是左上角的纵轴坐标，即y1
            b = math.floor(split_colsize * (Num_vertical - math.floor(Num_vertical)) - 0.2 * split_colsize / 2) + 0.8 * split_colsize * j
            # col_j是右下角的纵轴坐标，即y2
            col_j = b + split_colsize
            print("可舍弃的情况: b, col_j = [%s, %s]" % (b, col_j))

            part_img = img[int(math.floor(b)):int(math.ceil(col_j)), int(math.floor(a)):int(math.ceil(row_i))]
            newFileName = image_pre + "_split" + x + "dy" + "-" + str(i) + str(j) + ext
            print("什么情况： ", newFileName)
            cv2.imwrite(Outpath + newFileName, part_img)

    else:
        for j in range(math.ceil(Num_vertical)):
            b = 0.8 * split_colsize * j
            col_j = b + split_colsize
            if j == math.floor(Num_vertical):
                b = sum_cols - split_colsize
                col_j = sum_cols
            print("重叠覆盖的情况: b, col_j = [%s, %s]" % (b, col_j))

            part_img = img[int(math.floor(b)):int(math.ceil(col_j)), int(math.floor(a)):int(math.ceil(row_i))]
            newFileName = image_pre + "_split" + x + "-" + str(i) + str(j) + ext
            print("啥玩意： ", newFileName)
            cv2.imwrite(Outpath + newFileName, part_img)

'''此处的split_rowsize, split_colsize根据裁剪需要修改'''
def Split_Img(img, fileName, split_rowsize=1000, split_colsize=1000 , row_dif=None, col_dif=None, Outpath=None):
    image_pre, ext = os.path.splitext(fileName)

    sum_cols = img.shape[0]   # the image height
    sum_rows = img.shape[1]   # the image length
    print("sum_cols, sum_rows = [%s, %s]" % (sum_cols, sum_rows))

    Num_vertical = (sum_rows - 0.2 * split_rowsize) / (0.8 * split_rowsize)   # Num_vertical表示纵行的数量，同一纵行的x是不变的
    Num_horizontal = (sum_cols - 0.2 * split_colsize) / (0.8 * split_colsize)   # Num_horizontal表示横行的数量，同一横行的y是不变的
    print("Num_horizontal, Num_vertical = [%s, %s]" % (Num_horizontal, Num_vertical))

# 覆盖不全且未被覆盖部分可舍弃的情况
    if split_rowsize * (Num_horizontal - math.floor(Num_horizontal)) - 0.2 * split_rowsize < row_dif:
        for i in range(math.floor(Num_horizontal)):
            # a是左上角的横轴坐标，即x1
            a = math.floor(split_rowsize * (Num_horizontal - math.floor(Num_horizontal)) - 0.2 * split_rowsize / 2) + 0.8 * split_rowsize * i
            # row_i是右下角的横走坐标，即x2
            row_i = a + split_rowsize
            print("\n=================================="); print("可舍弃的情况: a, row_i = [%s, %s]"%(a, row_i)); print(">>>>>>>>>>>>>>>>>>>>>>")

            Col_split(img, image_pre, ext, a, row_i, sum_cols, Num_vertical, split_colsize, col_dif, Outpath, i, "dx")

# 覆盖不全且未被覆盖部分不可舍弃，需要重叠覆盖的情况
    else:
        for i in range(math.ceil(Num_horizontal)):
            a = 0.8 * split_rowsize * i
            row_i = a + split_rowsize
            if i == math.floor(Num_horizontal):
                a = sum_rows - split_rowsize
                row_i = sum_rows
            print("\n=================================="); print("重叠覆盖的情况: a, row_i = [%s, %s]" % (a, row_i)); print(">>>>>>>>>>>>>>>>>>>>>>")

            Col_split(img, image_pre, ext, a, row_i, sum_cols, Num_vertical, split_colsize, col_dif, Outpath, i, "")

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
        Split_Img(img1, fileName, row_dif=50, col_dif=50, Outpath=Outpath)


if __name__ == '__main__':
    InFile_path = "image_in"
    OutFile_path = "image_out"
    mkdir(OutFile_path)

    imgae_re = glob.glob('image_out/*')
    for i in imgae_re: os.remove(i)

    for Parent, Dir_Name, File_Name in os.walk(InFile_path):
        # 有子文件
        # for dirname in Dir_Name:
        #     Imgpath = InFile_path + '\\' + dirname
        #     Outpath = OutFile_path + '\\' + dirname
        #     InFile_do(Imgpath, Outpath)

        # 没有子文件
        InFile_do(InFile_path, OutFile_path)



