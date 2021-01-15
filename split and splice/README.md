## 数据预处理：拆分图像与标签

-[x] 拆分图像及其对应的标签，运行脚本：`split_main.py`
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
-[x] 只拆分图像，运行脚本：`split_image.py`
-[x] 只拆分标签，运行脚本：`split_xml.py`
