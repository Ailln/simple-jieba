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
Loading model cost 0.682 seconds.
Prefix dict has been built succesfully.

## pku | jieba
>> all: 1109949, true: 871705, false: 238244, acc: 0.7853559037397214
>> [calc] run time: 0:00:09.356500

## pku | simjb
>> all: 1109949, true: 890836, false: 219113, acc: 0.8025918307958294
>> [calc] run time: 0:00:07.936405

## msr | jieba
>> all: 2368422, true: 1908851, false: 459571, acc: 0.8059589887275156
>> [calc] run time: 0:00:18.218636

## msr | simjb
>> all: 2368422, true: 1929606, false: 438816, acc: 0.8147222074444503
>> [calc] run time: 0:00:13.357152

```

