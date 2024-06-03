import pickle
import json
import re
from datetime import timezone,datetime,timedelta
from zoneinfo import ZoneInfo

def initDict():
    dict = {}
    # 清空判重字典
    with open("./data/dict.pkl", "wb") as f:
        pickle.dump(dict, f)
    # 清空提交判重字典
    with open("./data/dictSubmission.pkl", "wb") as f:
        pickle.dump(dict, f)


# 向pta发送请求时的header，不用变就行，直接从浏览器里粘贴来的
def getHeaders():
    cfg={}
    with open("./config/cfg.json","r",encoding="utf-8") as f:
        cfg=json.load(f)
    # 从配置文件读取数据
    problemId=cfg['contest_id']
    cookie=cfg['cookie']
    # 从浏览器复制的header
    headers={
        "Accept": "application/json;charset=UTF-8",
        "Accept-Encoding":"gzip, deflate, br, zstd",
        "Accept-Language":"zh-CN",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": cookie,
        "Eagleeye-Pappname": "eksabfi2cn@94d5b8dc408ab8d",
        "Eagleeye-Sessionid": "3wlLtwL4j0X5772F1ymv1jt2bv0O",
        "Eagleeye-Traceid": "3f793bf1171646202705810238ab8d",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://pintia.cn/problem-sets/"+problemId+"/rankings",
        "Sec-Ch-Ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "X-Lollipop": "fd0f671d1f29b275fdfb4df1999ef66a",
        "X-Marshmallow": ""
    }
    return headers



# 将iso标准时间改为东八区时间
def transTimeformat(time_str):
    # 使用正则表达式匹配ISO 8601时间字符串中的时区偏移部分
    match = re.search(r'([+-]\d{2}):?(\d{2})$', time_str)
    
    if match:
        # 提取时区偏移的小时和分钟
        hours, minutes = map(int, match.groups())
        # 应用正确的时区偏移
        dt = datetime.fromisoformat(time_str.replace(match.group(), ""))
        dt = dt.replace(tzinfo=timezone(timedelta(hours=hours, minutes=minutes)))
    else:
        # 如果没有找到时区偏移，则假设为UTC
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
    
    # 转换为UTC时间
    dt = dt.astimezone(ZoneInfo("Asia/Shanghai"))
    dt = dt.strftime("%Y/%m/%d %H:%M:%S")
    return dt