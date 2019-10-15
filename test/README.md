# 测试

## 1. 安装依赖

```bash
$ cd simple-jieba/test
$ pip install -r requirements.txt
```

## 2. 下载数据集

```bash
$ wget http://sighan.cs.uchicago.edu/bakeoff2005/data/icwb2-data.zip
$ unzip icwb2-data.zip
```

## 3. 运行

```bash
$ python test_jieba_and_simjb.py

Building prefix dict from the default dictionary ...
Loading model from cache /var/folders/dn/0w0vd2hd5m7byx0t73yxrt700000gn/T/jieba.cache
Loading model cost 0.708 seconds.
Prefix dict has been built succesfully.

## pku | jieba
>> all: 1129003, true: 890761, false: 238242, acc: 0.7889801887151762
>> [calc] run time: 0:00:09.445523

## pku | simjb
>> all: 1129003, true: 881348, false: 247655, acc: 0.7806427440848253
>> [calc] run time: 0:00:07.100070

## msr | jieba
>> all: 2370974, true: 1822646, false: 548328, acc: 0.7687330185822366
>> [calc] run time: 0:00:17.768981

## msr | simjb
>> all: 2370974, true: 1929210, false: 441764, acc: 0.8136782604954756
>> [calc] run time: 0:00:13.634663
```

