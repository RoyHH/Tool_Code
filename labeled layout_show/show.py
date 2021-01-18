import os
import xml.dom.minidom
import cv2 as cv
import glob

def mkdir(path):
    # 判断路径是否存在，若不存在则创建
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)

def main():
    # 图片路径
    ImgPath = 'Img/'
    # ImgPath = '../split and splice/image_out_m/'
    # 标签路径
    AnnoPath = 'Anno/'
    # AnnoPath = '../split and splice/xml_out_m/'

    mkdir("layout_show/")
    imgae_re = glob.glob('layout_show/*')
    for i in imgae_re: os.remove(i)

    imagelist = os.listdir(ImgPath)
    for image in imagelist:

        image_pre, ext = os.path.splitext(image)
        imgfile = ImgPath + image
        xmlfile = AnnoPath + image_pre + '.xml'

        # 打开xml文档
        DOMTree = xml.dom.minidom.parse(xmlfile)
        # 得到文档元素对象
        collection = DOMTree.documentElement
        # 读取图片
        img = cv.imread(imgfile)

        filenamelist = collection.getElementsByTagName("filename")
        filename = filenamelist[0].childNodes[0].data
        print(filename)
        # 得到标签名为object的信息
        objectlist = collection.getElementsByTagName("object")

        for objects in objectlist:
            # 每个object中得到子标签名为name的信息
            namelist = objects.getElementsByTagName('name')
            # 通过此语句得到具体的某个name的值
            objectname = namelist[0].childNodes[0].data

            bndbox = objects.getElementsByTagName('bndbox')
            for box in bndbox:
                x1_list = box.getElementsByTagName('xmin')
                x1 = int(x1_list[0].childNodes[0].data)
                y1_list = box.getElementsByTagName('ymin')
                y1 = int(y1_list[0].childNodes[0].data)
                x2_list = box.getElementsByTagName('xmax')
                x2 = int(x2_list[0].childNodes[0].data)
                y2_list = box.getElementsByTagName('ymax')
                y2 = int(y2_list[0].childNodes[0].data)
                cv.rectangle(img, (x1, y1), (x2, y2), (44, 125, 222), thickness=5)
                cv.putText(img, objectname, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 1, (225, 169, 36),
                           thickness=3)
                # cv.imshow('head', img)    #尽量不要每张都展示，没啥用

            cv.imwrite("layout_show/"+ image_pre+ ".jpg", img)   #save picture

if __name__ == '__main__':
   main()

   ImgPath = "Img/"
   outpatch = "1/"

   imagelist = os.listdir(ImgPath)
   for image in imagelist:
        image_pre, ext = os.path.splitext(image)
        imgfile = ImgPath + image

        img = cv.imread(imgfile)

        part_img = img[0:100, 0:300]

        print("part_img = img[0:100, 0:300]")

        cv.imwrite(outpatch + image_pre + ".jpg", part_img)