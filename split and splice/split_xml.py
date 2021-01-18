# coding:utf-8
import os
import os.path
import cv2
import xml.dom.minidom
import xml.etree.ElementTree as ET
import shutil
import numpy as np

def box_dis_save(x1, y1, x2, y2, objects):
    bndbox = objects.findall('bndbox')
    for box in bndbox:
        x1_list = box.find('xmin'); xmin = int(x1_list.text)
        y1_list = box.find('ymin'); ymin = int(y1_list.text)
        x2_list = box.find('xmax'); xmax = int(x2_list.text)
        y2_list = box.find('ymax'); ymax = int(y2_list.text)

        print("xmin, ymin, xmax, ymax = [%s, %s, %s, %s]" % (
            xmin, ymin, xmax, ymax))

        x1_xmin = 1 if x1 <= xmin else 0
        x1_xmax = 1 if x1 <= xmax else 0
        x2_xmin = 1 if x2 >= xmin else 0
        x2_xmax = 1 if x2 >= xmax else 0

        y1_ymin = 1 if y1 <= ymin else 0
        y1_ymax = 1 if y1 <= ymax else 0
        y2_ymin = 1 if y2 >= ymin else 0
        y2_ymax = 1 if y2 >= ymax else 0

        print("x1, y1, x2, y2 = [%s, %s, %s, %s]" % (
            x1, y1, x2, y2))

        # discriminant vector
        dis_vec = [x1_xmin, x1_xmax, x2_xmin, x2_xmax, y1_ymin, y1_ymax, y2_ymin, y2_ymax]
        print("dis_vec = ", dis_vec)

        box_split = []
# 角处重叠
        if dis_vec[:4].count(1) * dis_vec[4:].count(1) == 9:
            # box_split = [ (1 - x1_xmin) * x1 + x1_xmin * xmin, (1 - y1_ymin) * y1 + y1_ymin * ymin,
            #               (1 -x2_xmax) * x2 + x2_xmax * xmax, (1 -y2_ymax) * y2 + y2_ymax * ymax]
            # print("box_split_corner = ", box_split)
            save_dis = 1

# 边处重叠
        elif dis_vec[:4].count(1) * dis_vec[4:].count(1) == 12:
            # zero_address = dis_vec.index(0)
            # print("zero_address = ", zero_address)
            # 0：x1>xmin 最左侧不在，3：x2<max 最右侧不在，4：y1>ymin 最上侧不在，7：y2<ymax 最下侧不在
            # box_split = [ (1 - x1_xmin) * x1 + x1_xmin * xmin,  (1 - y1_ymin) * y1 + y1_ymin * ymin,
            #               (1 - x2_xmax) * x2 + x2_xmax * xmax, (1 -y2_ymax) * y2 + y2_ymax * ymax]
            # print("box_split_side = ", box_split)
            save_dis = 2

# 全包重叠
        elif dis_vec.count(0) == 0:
            # box_split = [xmin, ymin,
            #              xmax, ymax]
            # print("box_split_inside = ", box_split)
            save_dis = 3

# 不重叠
        else:
            print("box_split_no")
            #  删除节点
            save_dis = 0

        if save_dis != 0:
            box_split = [(1 - x1_xmin) * x1 + x1_xmin * xmin - x1, (1 - y1_ymin) * y1 + y1_ymin * ymin - y1,
                         (1 - x2_xmax) * x2 + x2_xmax * xmax - x1, (1 - y2_ymax) * y2 + y2_ymax * ymax - y1]

            x1_list.text = str(int(box_split[0]))
            y1_list.text = str(int(box_split[1]))
            x2_list.text = str(int(box_split[2]))
            y2_list.text = str(int(box_split[3]))
            print("xmin_g, ymin_g, xmax_g, ymax_g = [%s, %s, %s, %s]" % (
                x1_list.text, y1_list.text, x2_list.text, y2_list.text))

            if save_dis == 1: print("box_split_corner = ")
            elif save_dis == 2: print("box_split_side = ")
            else: print("box_split_inside = ")
            print(box_split)

    return save_dis

def obeject_split(x1, y1, x2, y2, root):
    # 得到标签名为object的信息
    objectlist = root.findall("object")

    for objects in objectlist:
        print(">>>>>>>>>>>>>>>>>")
        # 每个object中得到子标签名为name的信息
        namelist = objects.find('name')
        # 通过此语句得到具体的某个name的值
        objectname = namelist.text
        print("object = ", objectname)

        # 对box坐标进行拆分条件进行distinguish,如果符合拆分条件，则对box拆分后save到新的xml
        result_dis = []
        result_dis = box_dis_save(x1, y1, x2, y2, objects)
        print('result_dis = ',result_dis)
        if result_dis == 0:
            root.remove(objects)
            print('remove成功')
        else:
            print('拆分成功')

def split_xmlfile(out_xml, xmlFile, xmlFile_split_new, x1=900, y1=900, x2=1500, y2=1500):
    # 打开xml文档
    dom = ET.parse(os.path.join(out_xml, xmlFile))
    # 得到文档元素对象
    root = dom.getroot()

    print("\n=============== filename ===============")
    filenamelist = root.find("filename")
    # print("filenamelist = ", filenamelist)
    filename = filenamelist.text
    print("filename = ", filename)
    xml_pre, ext = os.path.splitext(xmlFile_split_new)
    filenamelist.text = str(xml_pre)
    print("xmlFile_split_new = ", xml_pre)

    # 拆分object
    obeject_split(x1, y1, x2, y2, root)

    # 重写size
    sizelist = root.findall("size")
    for sizes in sizelist:
        # 每个object中得到子标签名为name的信息
        sizes.find('width').text = str(x2 - x1)
        sizes.find('height').text = str(y2 - y1)
        print("width = ", sizes.find('width').text)
        print("height = ", sizes.find('height').text)

    # 保存新xml文件
    dom.write(out_xml + "\\" + xmlFile_split_new)

    # 后处理，将不包含object的xml删除掉，以及把初始的xml删除掉
    del_noobj_dom = ET.parse(os.path.join(out_xml, xmlFile_split_new))
    del_noobj_root = del_noobj_dom.getroot()
    if del_noobj_root.find("object"): print("\n")
    else: os.remove(out_xml + "\\" + xmlFile_split_new)
    # os.remove(out_xml + "\\" + xmlFile)

if __name__ == "__main__":
    path_xml = 'xml_in'
    out_xml = 'xml_out'
    files_xml = sorted(os.listdir(path_xml))  # 得到文件夹下所有文件名称

    for xmlFile in files_xml:
        if not os.path.isdir(xmlFile):  # 判断是否是文件夹，不是文件夹才打开
            # print(xmlFile)
            shutil.copyfile(path_xml + "\\" + xmlFile, out_xml + "\\" + xmlFile)

            # 拆分后新图像的左上角(x1,y1)，和右上角(x2,y2)
            # x1 = 900;
            # x2 = 1500;
            # y1 = 900;
            # y2 = 1500

            xml_pre, ext = os.path.splitext(xmlFile)
            xmlFile_split_new = xml_pre + "hhhhh" + ext

            split_xmlfile(out_xml, xmlFile, xmlFile_split_new)


