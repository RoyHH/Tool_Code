import os, shutil
import sys

"""
需要满足以下条件：
1. 在JPEGImages中准备好图片
2. 在Label中准备好labels
3. 创建好如下所示的文件目录：
    - images
        - train2012
        - val2012
    - labels
        - train2012
        - val2012
"""
def Make_Dir(image_dir):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

def Make_for_torch_Yolov3(dir_image,
                                 dir_label,
                                 dir1_train,
                                 dir1_val,
                                 dir2_train,
                                 dir2_val,
                                 main_trainval,
                                 main_test):
    Make_Dir(dir1_train)
    Make_Dir(dir1_val)
    Make_Dir(dir2_train)
    Make_Dir(dir2_val)

    with open(main_trainval, "r") as f1:
        for line in f1:
            print(line[:-1], '\r', end="")
            sys.stdout.flush()

            # print(os.path.join(dir_image, line[:-1]+".jpg"), os.path.join(dir1_train, line[:-1]+".jpg"))
            shutil.copy(os.path.join(dir_image, line[:-1]+".jpg"),
                        os.path.join(dir1_train, line[:-1]+".jpg"))
            shutil.copy(os.path.join(dir_label, line[:-1]+".txt"),
                        os.path.join(dir2_train, line[:-1]+".txt"))

    with open(main_test, "r") as f2:
        for line in f2:
            print(line[:-1], '\r', end="")
            sys.stdout.flush()
            shutil.copy(os.path.join(dir_image, line[:-1]+".jpg"),
                        os.path.join(dir1_val, line[:-1]+".jpg"))
            shutil.copy(os.path.join(dir_label, line[:-1]+".txt"),
                        os.path.join(dir2_val, line[:-1]+".txt"))

# if __name__ == "__main__":
#     '''
#     https://github.com/ultralytics/yolov3
#     这个pytorch版本的数据集组织
#     - images
#         - train2012 # dir1_train
#         - val2012 # dir1_val
#     - labels
#         - train2012 # dir2_train
#         - val2012 # dir2_val
#     trainval.txt, test.txt 是由create_main.py构建的
#     '''
#
#     dir_image = r"data/VOCdevkit/VOC2012/JPEGImages"
#     dir_label = r"data/VOCdevkit/VOC2012/Label"
#
#     dir1_train = r"data/images/train2012"
#     dir1_val = r"data/images/val2012"
#
#     dir2_train = r"data/labels/train2012"
#     dir2_val = r"data/labels/val2012"
#
#     main_trainval = r"data/VOCdevkit/VOC2012/ImageSets/Main/trainval.txt"
#     main_test = r"data/VOCdevkit/VOC2012/ImageSets/Main/test.txt"
#
#
#     make_for_torch_yolov3(dir_image,
#                             dir_label,
#                             dir1_train,
#                             dir1_val,
#                             dir2_train,
#                             dir2_val,
#                             main_trainval,
#                             main_test)