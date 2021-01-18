# coding:utf-8
import os
import os.path
import cv2
import xml.dom.minidom
import xml.etree.ElementTree as ET
import shutil
import numpy as np
import glob


def mkdir(path):
    # 判断路径是否存在，若不存在则创建
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)

def check_xmlfile(out_xml, xmlFile, path_image):
    # 打开xml文档
    dom = ET.parse(os.path.join(out_xml, xmlFile))
    # 得到文档元素对象
    root = dom.getroot()

    print("\n=============== filename ===============")
    filenamelist = root.find("filename")
    # print("filenamelist = ", filenamelist)
    filename = filenamelist.text
    print("filename = ", filename)

    image_pre, ext = os.path.splitext(xmlFile)
    img = cv2.imread(path_image + "\\" + image_pre + '.jpg')
    h = img.shape[0]   # the image height
    w = img.shape[1]   # the image length

    # 重写size
    sizelist = root.findall("size")
    for sizes in sizelist:
        # 每个object中得到子标签名为name的信息

        if sizes.find('width').text > str(w):
            sizes.find('width').text = str(w)
            print("width 修改成功")

        if sizes.find('height').text > str(h):
            sizes.find('height').text = str(h)
            print("height 修改成功")

        # 保存新xml文件
        dom.write(out_xml + "\\" + xmlFile)

if __name__ == "__main__":
    path_xml = 'xml_out_m'
    path_image = 'image_out_m'
    out_xml = 'xml_out_m_check'
    mkdir(out_xml)
    files_xml = sorted(os.listdir(path_xml))  # 得到文件夹下所有文件名称

    xml_re = glob.glob('xml_out_m_check/*')
    for i in xml_re: os.remove(i); print("i = ", i)

    for xmlFile in files_xml:
        if not os.path.isdir(xmlFile):  # 判断是否是文件夹，不是文件夹才打开
            # print(xmlFile)
            shutil.copyfile(path_xml + "\\" + xmlFile, out_xml + "\\" + xmlFile)

            check_xmlfile(out_xml, xmlFile, path_image)