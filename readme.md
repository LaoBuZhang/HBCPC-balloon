# 河北省省赛气球打印系统

本系统是2024年CCPC河北省省赛是使用的气球打印系统

省赛使用的是pta系统，因此本系统只能在使用pta进行比赛时使用

本程序是将pta的数据爬取下来并判重打印

本程序使用的打印机时易联云打印机，使用其他的打印机需要对代码进行修改（具体后文会说到）

作者：laobuzhang


## 使用说明
其中有多个py文件，作用如下：
- balloon_functions.py
    - 主要函数文件，存放要使用到的函数
- balloon_main.py
    - main文件，比赛开始后，运行此文件即可快开始打印气球信息
    - 若中途意外中断运行，重新运行此代码即可，已经写过中断处理
- balloon_printer.py
    - 使用易联云打印机进行打印的代码
    - 易联云打印机的sdk在Lib文件夹中
    - 如果想要使用其它的打印机，则需要修改此文件，可以只修改其中的两个函数内容即可
      - generate_order_number()函数是生成一个打印编号，如果你的打印机不需要的话可以不用这个函数
      - printer()函数是打印函数，需要打印"./data/printer.txt"文件中的内容并将打印任务发送给打印机
- balloon_utils.py
   - 一些工具函数


## 易联云打印机
需要在[易联云打印机管理系统](https://dev.10ss.net/admin)创建一个自有型应用，并和自己的打印机绑定

在应用信息中拿到
- 用户id
- 应用id
- 应用密钥



## 配置文件
在config文件夹中，有两个配置文件，需要在运行前修改
- cfg.json
    - client_id：上文在易联云应用信息中拿到的应用id
    - client_secret：上文在易联云应用信息中拿到的应用密钥
    - machinne_id：打印机背面的终端号
    - start_time：比赛开始时间
    - contest_id: pta的比赛的id，可以直接进入比赛，在网址中找到比赛id
    - cookie: pta中拥有该比赛管理权限的账号的cookie，获取方式为登陆该账号，在f12中找到cookie并复制下来
- cfg_room.json
    - 赛场-教室对应文件
    - 我们比赛时使用了多个教室作为赛场，每个赛场有一个字母编号，每一个教室有一个门牌号



## 运行环境
我使用的时vscode，安装了coderunner插件，直接右键 run code就能运行程序

同时安装了python3.10

使用到了一些第三方包，需要自己pip install（有些包的名字和安装时使用的名字不一样，所以尽量查一查）



## pta队伍创建
程序直接爬取的PTA榜单，其中的用户由管理员创建

适配该程序的格式如下：
- PTA学号：
    - 比赛缩写+年份+"-"+赛场+赛场内座位号
    - 例如：`HBCPC2024-A01`
- 队伍名：
    - 学校名+"_"+队伍名
    - 例如：`小汤河职业技术学院_鸡你太美队`



## 使用方式

1. 第一次运行运行main.py：`python -u main.py`（有code runner直接右键run code）
2. 运行途中意外中断的话，重新运行main.py：`python -u restartMain.py`即可，有写中断处理