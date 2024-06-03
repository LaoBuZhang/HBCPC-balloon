import os
import balloon_functions
import balloon_utils
import time
import json
import pickle
from datetime import datetime



if __name__ == '__main__':
    # 读取配置文件
    cfg={}
    with open('./config/cfg.json', 'r') as f:
        cfg = json.load(f)

    # 读入room配置文件
    roomDict={}
    with open("./config/cfg_room.json", 'r', encoding='utf-8') as roomFile:
        roomDict = json.load(roomFile)

    contest_id=cfg['contest_id']


    # 使用到的字典文件，不存在则创建出来
    dict={}
    if not os.path.exists("./data/dict.pkl"):
        with open("./data/dict.pkl", 'wb') as f:
            pickle.dump(dict, f)
    if not os.path.exists("./data/dictSubmission.pkl"):
        with open("./data/dictSubmission.pkl", 'wb') as f:
            pickle.dump(dict, f)
    
    # 如果在比赛开始前运行的话，每次都会清空字典
    # 如果在比赛开始后运行的话，每次不会清空字典
    current_time = datetime.now()
    format_str = "%Y-%m-%d %H:%M:%S"
    start_time = datetime.strptime(cfg['start_time'],format_str)
    if current_time<start_time:
        balloon_utils.initDict()


    i=0
    while True:
        i=i+1
        if(i%8==0):# 每爬取8次，从第一条爬取一次，获取到爬取时正在评测的数据
            i=0
            print("=================spider from start=================")
            balloon_functions.spider(contest_id,roomDict,True)
        else:
            print("=================spider from before================")
            balloon_functions.spider(contest_id,roomDict,False)
        print("忙了半天了，让我歇一会！！！")
        time.sleep(15)