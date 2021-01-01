## 1. 数据集搭建

- [x] 按需修改相关路径后，运行脚本：`main.py`

所用到的功能封装在`main.py`中，下面依次介绍

- 特殊性说明：

我自己搭建的数据集，原始排放方式如下

```
- data
    - New Data-jpg
        - IGBT_PIC（存放原始图片样本）
            - IGBT_fiber_3
                - 201117_111036
                    - 201117_111036_0000000541_CAM1_NG.jpg
                    ... ...
                ... ...
            ... ...
        - Labels (存放原始图片样本对应的标签)
            - IGBT_fiber_3
                - 201117_111036
                    - 201117_111036_0000000541_CAM1_NG.xml
                    ... ...
                ... ...
            ... ...
        - 数据采集记录.xlsx
```

需要整理一下，贴近voc2012数据集存放逻辑，以便使用`main.py`

- [x] 脚本：`for_IGBTdataset.py`

整理后，如下

```
- data
    - New Data-jpg
        - IGBT_PIC（存放原始图片样本）
        - Labels (存放原始图片样本对应的标签)
        - 数据采集记录.xlsx
        - IGBT_Img（存放整理后的图片样本）
            - 201117_111036_0000000541_CAM1_NG.jpg
            ... ...            
        - IGBT_Labels (存放整理后的图片样本对应的标签)
            - 201117_111036_0000000541_CAM1_NG.xml
            ... ... 
```

### 1.1. 数据集检查

以下是一个标准的voc2012数据集文件排放方式。

```
- data
    - VOCdevkit
        - VOC2012
        - Annotations (标签XML文件，用对应的labelimg生成的)
        - ImageSets (生成的方法是用python生成)
            - Main
                - test.txt
                - train.txt
                - trainval.txt
                - val.txt
        - JPEGImages(原始文件)
```

其中JPEGImages中的图片与Annotations中的xml文件个数应该是一致且一一对应的关系。

这里创建了一个简单的脚本进行评估一致性,需要建立新的文件夹Allempty， 意思是以xml文件为基准进行图片检查，如果图片不存在对应xml文件，那将图片移动到Allempty文件夹中。

- [x] 脚本：`check_jpgAndxml.py`

### 1.2. 按照比例划分训练/测试/验证集合

- [x] 脚本：`train_test_val.py`

trainval_percent: 表示训练集和验证集占所有图片的比例。(train+val)/(train+val+test)

train_percent: 表示训练集占训练集和验证集的比例。(train)/(train+val)

### 1.3. 根据xml文件生成Label文件夹中的txt文件

- [x] 脚本：`voc_label.py`

### 1.4. 构建数据集所需的文件，按照pytorch版本的要求进行整理

- [x] 脚本：`make_for_yolov3_torch.py`

最后文件夹构成：

```
- data
    - VOCdevkit
        - VOC2012
            - Annotations (标签XML文件，用对应的labelimg生成的)
            - ImageSets (生成的方法是用python生成)
                - Main
                    - test.txt
                    - train.txt
                    - trainval.txt
                    - val.txt
            - JPEGImages(原始文件)
    - Label (xml文件对应的txt文件)
    - images (用于pytorch版本的图片保存)
        - train2012
            - 001.jpg
            - 002.jpg
        - val2012
            - 100.jpg
            - 101.jpg
    - labels (用于pytorch版本的标签保存)
        - train2012
            - 001.txt
            - 002.txt
        - val2012
            - 100.txt
            - 101.txt
    - VOC2012_test.txt
    - VOC2012_train.txt
    - VOC2012_val.txt
```

我自己搭建的数据集，最后文件夹构成：

```
- data
    - New Data-jpg
        - IGBT_PIC（存放原始图片样本）
        - Labels (存放原始图片样本对应的标签)
        - 数据采集记录.xlsx
        - IGBT_Img（存放整理后的图片样本）        
        - IGBT_Labels (存放整理后的图片样本对应的标签)
        - Main
            - test.txt
            - train.txt
            - trainval.txt
            - val.txt
    - images (用于pytorch版本的图片保存)
        - train2021
            - xxxxx.jpg
            ... ...   
        - val2021
            - xxxxx.jpg
            ... ...
    - labels (用于pytorch版本的标签保存)
        - train2021
            - xxxxx.txt
            ... ...
        - val2021
            - xxxxx.txt
            ... ...
    - IGBT_DF2021_test.txt
    - IGBT_DF2021_train.txt
    - IGBT_DF2021_val.txt
```

## 2. 将构建好的数据集，放到Yolo v3对应的文件夹中

- [x] 将本项目`data`文件夹中`images`，`labels`文件夹放到Yolo v3的`data`文件夹里
- [x] 将本项目`data`文件夹中`VOC2012_train.txt`，`VOC2012_test.txt`文件放到Yolo v3的`data`文件夹里
- [x] 修改本项目`data`文件夹中的`template.names`，里边就是classes内容，每行一个类别，最后放到Yolo v3的`data`文件夹里
- [x] 修改本项目`data`文件夹中的`template.data`文件，填入相应内容(注意这个文件中用”valid=“而不是”test=“是因为需要与Yolo v3对应，不过实际上用的是test数据集)
- [x] 修改`Yolo v3/train.py`中的argparse部分的`coco.data`为`template.data`(或自己的命名的data文件)
- [x] 修改`Yolo v3/cfg`中使用网络的对应cfg文件，参考[Train Custom Data/5](https://github.com/ultralytics/yolov3/wiki/Train-Custom-Data)
- [x] 严格按照以上步骤进行执行即可运行

`template.data`文件中的内容如下

```
classes=20
train=data/VOC2012_train.txt
valid=data/VOC2012_test.txt
names=data/template.names
```

## 3. 一些细节

批量修改xml标签中的类别名称

- [x] 脚本：`change_annotations_classname.py`

voc格式的xml，转为coco格式的json

- [x] 脚本：`voc2coco.py`