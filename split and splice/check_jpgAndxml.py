import os, shutil
from tqdm import *

def Check_JpgXml(jpeg_dir, annot_dir):
    """
    dir1 是图片所在文件夹
    dir2 是标注文件所在文件夹
    """
    pBar = tqdm(total=len(os.listdir(jpeg_dir)))
    cnt = 0
    for file in os.listdir(jpeg_dir):
        pBar.update(1)
        f_name, f_ext = file.split(".")
        if not os.path.exists(os.path.join(annot_dir, f_name + ".xml")):
            print(f_name)
            cnt += 1

            os.remove(jpeg_dir + '/' + f_name + ".jpg")
            # print("删除“图片和对应的xml”不匹配的文件 %s"%(jpeg_dir + '/' + f_name + ".jpg"))

    pBar1 = tqdm(total=len(os.listdir(annot_dir)))
    cnt1 = 0
    for file in os.listdir(annot_dir):
        pBar1.update(1)
        f_name, f_ext = file.split(".")
        if not os.path.exists(os.path.join(jpeg_dir, f_name + ".jpg")):
            print(f_name)
            cnt1 += 1

            os.remove(annot_dir + '/' + f_name + ".xml")
            # print("删除“图片和对应的xml”不匹配的文件 %s"%(annot_dir + '/' + f_name + ".xml"))

    if cnt > 0:
        print("有%d个文件不符合要求。" % (cnt1))
    else:
        print("所有图片和对应的xml文件都是一一对应的。")


# if __name__ == "__main__":
#     dir1 = r"data/VOCdevkit/VOC2012/JPEGImages"
#     dir2 = r"data/VOCdevkit/VOC2012/Annotations"
#     checkJpgXml(dir1, dir2)