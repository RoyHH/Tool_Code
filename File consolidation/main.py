import os
import shutil

def mkdir(path):
    # 判断路径是否存在，若不存在则创建
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)

def read_dir(InFile_path, OutFile_path):
    for direname in os.listdir(InFile_path):
        Outpath_jpg = OutFile_path + '\\' + direname + '_jpg'
        Outpath_xml = OutFile_path + '\\' + direname + '_xml'
        mkdir(Outpath_jpg)
        mkdir(Outpath_xml)

        Imgpath = InFile_path + '\\' + direname
        for dir_child in os.listdir(Imgpath):
            child_jpg = Outpath_jpg + '\\' + dir_child
            child_xml = Outpath_xml + '\\' + dir_child
            mkdir(child_jpg)
            mkdir(child_xml)

            child_in = Imgpath + '\\' + dir_child
            csd_file(child_in, child_jpg, child_xml)

def csd_file(child_in, child_jpg, child_xml):
    for fileName in os.listdir(child_in):
        if os.path.splitext(fileName)[1] == '.jpg':
            x = child_in + '\\' + fileName
            y = child_jpg + '\\' + fileName
            shutil.copy(x, y)
        if os.path.splitext(fileName)[1] == '.xml':
            x = child_in + '\\' + fileName
            y = child_xml + '\\' + fileName
            shutil.copy(x, y)


def main():
    InFile_path = "original file"
    OutFile_path = "out"
    read_dir(InFile_path, OutFile_path)

    # for Parent, Dir_Name, File_Name in os.walk(InFile_path):
    #     for direname in Dir_Name:
    #         Imgpath = InFile_path + '\\' + direname
    #         Outpath_jpg = OutFile_path + '\\' + direname + '_jpg'
    #         Outpath_xml = OutFile_path + '\\' + direname + '_xml'
    #
    #         mkdir(Outpath_jpg)
    #         mkdir(Outpath_xml)

if __name__ == '__main__':
   main()