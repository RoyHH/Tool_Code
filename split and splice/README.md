## 数据预处理：拆分图像与标签
- [x] 拆分图像及其对应的标签，运行脚本：`split_main.py`
> 其中`row_dif`和`col_dif`表示横向与纵向可以舍弃的边的像素值，我设置为50
```
Split_Img(img1, fileName, row_dif=50, col_dif=50, Outpath=Outpath)
```
> `split_rowsize`和`split_colsize`表示需要拆分成图像的大小，我设置为1000
```
split_rowsize=1000, split_colsize=1000
```
>这里的小图（原图被拆分后的子图）与临近小图间是有重叠的，重叠的比例我设置为20%
```
Num_vertical = (sum_rows - 0.2 * split_rowsize) / (0.8 * split_rowsize)  
Num_horizontal = (sum_cols - 0.2 * split_colsize) / (0.8 * split_colsize)  
```
- [x] 只拆分图像，运行脚本：`split_image.py`
- [x] 只拆分标签，运行脚本：`split_xml.py`

## 流程
>copy file
>>split images and save images
>>>split xmls and save xmls
>>>>check width and height between xml with image

## 备注：几点说明
- 有些地方不够严谨，拆分时会有一些问题，如下：
```
Num_vertical = (sum_rows - 0.2 * split_rowsize) / (0.8 * split_rowsize)  
Num_horizontal = (sum_cols - 0.2 * split_colsize) / (0.8 * split_colsize)  
```
>这里用的公式，是我设计的，不过会造成拆分到大图边缘的最后一张临界图有可能会超限，
>从而导致image中的尺寸与xml中记录的尺寸不一致，这里说的尺寸是指width和height（对标签的坐标不会造成影响），
>这个不一致会在做YOLO数据集时，对标签的相对坐标归一化造成影响，有可能导致回归框偏移。
>其解决办法有2，如下：

- [x] **方法1**

```
if row_i > img.shape[1]: row_i = img.shape[1]
if col_j > img.shape[0]: col_j = img.shape[0]  
part_img = img[b:col_j, a:row_i]   # img[y, x]
```
- [x] **方法2**
```
check_xmlfile(out_xml_check, xmlFile, OutFile_path)
```
>2者可以单独使用，也可以一起使用