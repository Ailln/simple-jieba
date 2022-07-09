# 性能测试

## 1. 安装依赖

```bash
cd simple-jieba/test
pip install -r requirements.txt
```

## 2. 下载数据

```bash
wget http://sighan.cs.uchicago.edu/bakeoff2005/data/icwb2-data.zip
unzip icwb2-data.zip
```

## 3. 运行测试

```bash
python performance_test.py

load freq_dict cost: 0.57s

Building prefix dict from the default dictionary ...
Loading model from cache /var/folders/d9/f92y4w355p7gz8f8p_0t9kbm0000gn/T/jieba.cache
Loading model cost 0.401 seconds.
Prefix dict has been built successfully.

## pku | jieba
>> all: 1109949, true: 871705, false: 238244, acc: 0.7854
[calc] run time(s): 6.4405

## pku | simjb
>> all: 1109949, true: 894347, false: 215602, acc: 0.8058
[calc] run time(s): 6.01619

## msr | jieba
>> all: 2368422, true: 1908851, false: 459571, acc: 0.8060
[calc] run time(s): 10.91983

## msr | simjb
>> all: 2368422, true: 1932899, false: 435523, acc: 0.8161
[calc] run time(s): 10.87769
```
