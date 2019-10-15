from time import ctime

from simjb.version import VERSION


def run():
    cur_time = ctime()
    text = f"""
    simjb: A simple version of jieba.
    
    https://github.com/HaveTwoBrush/simple-jieba

    Version {VERSION} ({cur_time} +0800)
    """
    print(text)
