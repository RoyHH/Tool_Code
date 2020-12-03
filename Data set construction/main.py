import os
import shutil

from check_jpgAndxml import Check_JpgXml
from train_test_val import Create_Main_Txts
from voc_label import Get_Voc_Lable
from make_for_yolov3_torch import Make_for_torch_Yolov3

if __name__ == "__main__":
    ###############################################################################
    # 0. 参数设置
    jpegimages_dir = r"data/VOCdevkit/VOC2012/JPEGImages"  # 图片保存位置
    annotations_dir = r"data/VOCdevkit/VOC2012/Annotations"  # 标注文件保存位置

    # 分为3份：train,val,test
    trainval_percent = 0.8  # (train+val)/(train+val+test)
    train_percent = 1  # (train)/(train+val)

    # 修改类别
    classes = ["person", "bird", "cat", "cow", "dog", "horse", "sheep",
               "aeroplane", "bicycle", "boat", "bus", "car", "motorbike", "train",
               "bottle", "chair", "dining table", "potted plant", "sofa",
               "tv/monitor"]  #修改为自己的类别，多个类["class1","class2"]

    dir_label = r"data/Label"

    dir1_train = r"data/images/train2012"
    dir1_val = r"data/images/val2012"
    dir2_train = r"data/labels/train2012"
    dir2_val = r"data/labels/val2012"

    main_trainval = r"data/VOCdevkit/VOC2012/ImageSets/Main/trainval.txt"
    main_test = r"data/VOCdevkit/VOC2012/ImageSets/Main/test.txt"

    ##################################################################################

    # 1. 检查jpg和xml文件是否是一一对应的
    print("=" * 5, "\t1. checking jpg and xml\t", "=" * 5)
    Check_JpgXml(jpeg_dir=jpegimages_dir, annot_dir=annotations_dir)

    # 2. 按照比例创建训练、验证、测试
    print("=" * 5, "\t2. split train, val, test\t", "=" * 5)
    Create_Main_Txts(trainval_percent=trainval_percent,
                     train_percent=train_percent)

    # 3. 将坐标进行归一化，生成labels中的txt文件
    print("=" * 5, "\t3. create txt files in labels\t", "=" * 5)
    Get_Voc_Lable(classes)

    # 4. 构建pytorch版本yolov3格式
    print("=" * 5, "\t4. create yolov3 format\t", "=" * 5)
    Make_for_torch_Yolov3(jpegimages_dir, dir_label, dir1_train, dir1_val,
                          dir2_train, dir2_val, main_trainval, main_test)

    # 5. 收尾，将中间文件删除
    print("=" * 5, "\t5. delete temporary directory\t", "=" * 5)

    if os.path.exists(dir_label):
        shutil.rmtree(dir_label)

    # images = r"data/images"
    # if os.path.exists(images):
    #     shutil.rmtree(images)
    #
    # labels = r"data/labels"
    # if os.path.exists(labels):
    #     shutil.rmtree(labels)

    # 6. 之后的操作：
    print("=" * 50)
    print("配套代码: https://github.com/ultralytics/yolov3")
    print("之后的操作：")
    print("1. 将本项目`data`文件夹中`images`，`labels`文件夹放到Yolo v3的`data`文件夹里")
    print("2. 将本项目`data`文件夹中`VOC2012_train.txt`，`VOC2012_test.txt`文件放到Yolo v3的`data`文件夹里")
    print("3. 修改本项目`data`文件夹中的`template.names`，里边就是classes内容，每行一个类别，最后放到Yolo v3的`data`文件夹里")
    print("4. 修改本项目`data`文件夹中的`template.data`文件，填入相应内容(注意这个文件中用”valid=“而不是”test=“是因为需要与Yolo v3对应，不过实际上用的是test数据集)")
    print("5. 修改`Yolo v3/train.py`中的argparse部分的`coco.data`为`template.data`(或自己的命名的data文件)")
    print("6. 修改`Yolov3 / cfg`中使用网络的对应cfg文件，参考https://github.com/ultralytics/yolov3/wiki/Train-Custom-Data")
    print("7. 严格按照以上步骤进行执行即可运行")
    print("=" * 50)


