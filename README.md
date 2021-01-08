## 1 异物检测

#### 1.1 数据（图像）采集与预处理

* 图像格式
```
采集到的图像，bmp和jpg格式可能都会有，所以需要将图像统一为一种格式
```
- [x] 脚本文件：`Bmp-Jpg`

* 图像纪要
```
采集工作中的图像信息纪要读取
```
- [x] 脚本文件：`Excel read`

* 图像尺寸
```
根据需求裁剪、拼接图像
```
- [x] 脚本文件：`split and splice`

#### 1.2 数据（图像）做标签与数据集整理

* 图像与标签文件归档
```
做完标签后的文件，存在图像与标签混在一起的问题，需分开存储
```
- [x] 脚本文件：`File consoildation`

* 验证标签的效用
```
在原图上展示标签信息
```
- [x] 脚本文件：`Labeled layout_show`

#### 1.3 对数据集按照Yolo v3输入格式进行梳理

- [x] 脚本文件：`Data set construction`

#### 1.4 对训练结果（Excel 文件）曲线展示

- [x] 脚本文件：`Draw Excel`

## 2 其他

```
利用opencv做逐像素对比
```
- [x] 脚本文件：`Different point`