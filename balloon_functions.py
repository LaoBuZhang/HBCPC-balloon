import gzip
import json
import codecs
import pickle
import urllib.request
import balloon_printer
import balloon_utils


# 整理数据，调用打印函数
def out(teamId,teamName,problemId,dict,roomDict):
    # 判重
    file = codecs.open('./data/printer.txt','w','UTF-8')
    ball_id=teamName+problemId
    if ball_id in dict:
        return
    dict[ball_id]=True
    # split
    file.write("----------------\n")
    file.write('BALLOON_STATUS\n')
    # 气球颜色
    str_str = "气球颜色："+problemId+"\n"
    file.write(str_str)
    # 赛场
    room=teamId[-3]
    if(room in roomDict):
        str_str = "赛场："+roomDict[room]+"\n"
    else:
        str_str = "赛场："+"测试赛场"+"\n"
    file.write(str_str)
    roomDict.clear()
    # 座位号
    str_str = "座位号："+teamId+"\n"
    file.write(str_str)
    # 团队名称
    str_str = "团队名称："+teamName+"\n"
    file.write(str_str)
    # spilt
    file.write("----------------")
    file.close()
    # 打印
    balloon_printer.printer()


# 根据编译器信息得到语言
def transComplierToLanguage(compiler):
    if compiler=='GXX' or compiler=='CLANGXX':
        return "C++"
    elif compiler=='GCC' or compiler=='CLANG':
        return "C"
    elif compiler=='PYPY3' or compiler=='PYTHON3' or compiler=='PYTHON2':
        return "Python"
    elif compiler=='JAVAC':
        return "Java"
    else:
        return "Other Language"


# 将接口得到的数据转换为想要的格式
def transDatas(submitList,problemList,userList):
    ans=[]
    for v in submitList:
        item={}
        item['submissionId']=v['id']
        item['submitAt']=balloon_utils.transTimeformat(v['submitAt'])
        item['status']=v['status']
        item['problemLabel']=problemList[v['problemSetProblemId']]['label']
        item['language']=transComplierToLanguage(v['compiler'])
        item['compiler']=v['compiler']
        item['memory']=int(v['memory']/1024)
        item['time']=v['time']
        item['teamPtaId']=userList[v['userId']]['studentUser']['studentNumber']
        item['teamName']=userList[v['userId']]['studentUser']['name']
        ans.append(item)
    return ans


def getNextSubmitList(contestId,id,ans,dictSubmission):
    print("request next page")
    # 请求提交列表的url
    url="https://pintia.cn/api/problem-sets/"+contestId+"/submissions?before="+id+"&limit=100&filter=%7B%7D"
    # 直接从浏览器复制的header
    headers=balloon_utils.getHeaders()
    # 发送请求
    req=urllib.request.Request(url,headers=headers)
    response=urllib.request.urlopen(req)
    # 解析请求
    content = gzip.decompress(response.read())
    data = content.decode('utf-8')
    json_data = json.loads(data)
    # 得到提交列表
    submitList=json_data['submissions']
    # 提交列表中涉及到的题目
    problemList=json_data['problemSetProblemById']
    # 提交列表中涉及到的用户的用户信息
    userList=json_data['examMemberByUserId']
    ansNext=transDatas(submitList,problemList,userList)
    # 通过字典判断是否继续爬取
    # 继续爬取返回最后一条数据的id，作为下一次爬取的before参数的值
    # 不继续爬取则返回空字符串
    if len(ansNext)!=0:
        if ansNext[len(ansNext)-1]['submissionId'] in dictSubmission:
            ans.extend(ansNext)
            return ""
    else:
        return ""

    if len(ansNext)==0:
        return ""
    else:
        ans.extend(ansNext)
        return ansNext[len(ansNext)-1]['submissionId']


def getSubmitList(contestId,dictSubmission):
    print("request first page")
    # 请求提交列表的url
    url="https://pintia.cn/api/problem-sets/"+contestId+"/submissions?limit=100&filter=%7B%7D"
    # 直接从浏览器复制的header
    headers=balloon_utils.getHeaders()
    # 发送请求
    req=urllib.request.Request(url,headers=headers)
    response=urllib.request.urlopen(req)
    # 解析请求
    content = gzip.decompress(response.read())
    data = content.decode('utf-8')
    json_data = json.loads(data)
    # 得到提交列表
    submitList=json_data['submissions']
    # 提交列表中涉及到的题目
    problemList=json_data['problemSetProblemById']
    # 提交列表中涉及到的用户的用户信息
    userList=json_data['examMemberByUserId']
    ans=transDatas(submitList,problemList,userList)

    # 通过字典判断是否继续爬取
    if len(ans)!=0:
        if ans[len(ans)-1]['submissionId'] in dictSubmission:
            return ans

    # 爬取后边页数
    id=""
    if len(ans)!=0:
        id=ans[len(ans)-1]['submissionId']
        id=getNextSubmitList(contestId,id,ans,dictSubmission)
        while id!="":
            id=getNextSubmitList(contestId,id,ans,dictSubmission)
    return ans

# 爬取数据
def spider(contestId,roomDict,fromStart):
    # 提交判重字典
    dictSubmission = {}
    with open("./data/dictSubmission.pkl", "rb") as f:
        dictSubmission = pickle.load(f)
    if fromStart:
        dictSubmission.clear()

    # 爬取数据并打印
    ans=getSubmitList(contestId,dictSubmission)
    print("printing......")
    for v in ans:
        dictSubmission[v['submissionId']]=True
        if v['status']=='ACCEPTED':
            # 判重字典
            dict = {}
            with open("./data/dict.pkl", "rb") as f:
                dict = pickle.load(f)

            # 打印数据
            out(v['teamPtaId'],v['teamName'],v['problemLabel'],dict,roomDict)

            # 写入提交判重字典
            with open("./data/dict.pkl", "wb") as f:
                pickle.dump(dict, f)
    
    # 写入判重字典
    with open("./data/dictSubmission.pkl", "wb") as f:
        pickle.dump(dictSubmission, f)