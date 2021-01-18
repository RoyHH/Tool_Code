import time
import os
import glob
import random
import cv2 as cv
import shutil


def mkdir(path):
    # 判断路径是否存在，若不存在则创建
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)

now_time = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))

in_path = "layout_show_m"
out_path = "Random_samples_m" + now_time
mkdir(out_path)

imgae_re = glob.glob(out_path + '/*')
for i in imgae_re: os.remove(i)

for Parent, Dir_Name, File_Name in os.walk(in_path):
    n = len(File_Name) / 4
    print("n = ", n)

    for i in range(int(n)):
        save_i = random.randint(0, 3) + i * 4
        print("save_i = ", save_i)
        print("File_Name[ %s ] = %s" % (str(save_i), str(File_Name[save_i])))

        shutil.copyfile(in_path + "\\" + File_Name[save_i], out_path + "\\" + File_Name[save_i])

