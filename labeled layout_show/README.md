## 标签标记展示
- [x] 运行脚本：`show.py`

## 数据筛选
- [x] 运行脚本：`Random_sample.py`
>联动`split and splice`模块（简称**SS**），利用**SS**生成的初始数据集，通过`show.py`展示出来，
>>再进行`Random_sample.py`筛选出一部分，用于作为搭建训练数据集的筛选基准数据集，
>>>最后使用这个筛选基准数据集，对照**SS**中生成的初始数据集，运行**SS**中的`check_jpgAndxml.py`，分别针对image和xml运行两次，
>>>>最终可得到训练数据集

