import os
import os.path
import cv2

def mkdir(path):
    # 判断路径是否存在，若不存在则创建
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)

def Bmp2Jpg(in_path, out_path):
    for fileName in os.listdir(in_path):
        if os.path.splitext(fileName)[1] == '.bmp':
            img = cv2.imread(in_path + "\\" + fileName)
            img1 = img.copy()
            # print(fileName.replace(".bmp", ".jpg"))
            newFileName = fileName[0:fileName.find(".bmp")] + ".jpg"
            print(newFileName)
            cv2.imwrite(out_path + "\\" + newFileName, img1)
        else:
            img = cv2.imread(in_path + "\\" + fileName)
            img2 = img.copy()
            print(fileName)
            cv2.imwrite(out_path + "\\" + fileName, img2)

def Delete_Images(in_path, imageFormat):
   command = "del "+in_path+"\\*."+imageFormat
   os.system(command)

def main():
   InFile_path = "E:\\PhD Projects\\Foreign Object Detection-BJ\\Data Store\\Original Data\\Organizing Data-cv-x"
   OutFile_path = "E:\\PhD Projects\\Foreign Object Detection-BJ\\Data Store\\Processed Data-jpg\\Data-jpg"

   mkdir(OutFile_path)

   for Parent, Dir_Name, File_Name in os.walk(InFile_path):
       for dirname in Dir_Name:
           in_path = InFile_path + "\\" +dirname
           out_path = OutFile_path + "\\" +dirname
           print(dirname)
           mkdir(out_path)
           Bmp2Jpg(in_path, out_path)
           # Delete_Images(path, "bmp")

if __name__ == '__main__':
   main()