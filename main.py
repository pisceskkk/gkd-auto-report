import requests
import time
import os

s = requests.Session()

GKD_EMAIL = os.environ["GKD_EMAIL"]    # sep账号
GKD_PASSWORD = os.environ["GKD_PASSWORD"]   # sep密码
GKD_NUMBER = os.environ["GKD_NUMBER"]
GKD_NAME = os.environ["GKD_NAME"]
PUSH_TOKEN = os.environ["PUSH_TOKEN"]
GEO_INFO_LIST = eval(os.environ["GEO_INFO_LIST"])
GEO_INFO_IDX = eval(os.environ["GEO_INFO_IDX"])
GEO_INFO_IDX_OLD = eval(os.environ["GEO_INFO_IDX_OLD"])
GEO_INFO = GEO_INFO_LIST[GEO_INFO_IDX]
GEO_INFO_OLD = GEO_INFO_LIST[GEO_INFO_IDX_OLD]

def login(s: requests.Session):
    r = s.post("https://app.ucas.ac.cn/uc/wap/login/check", data={
        "username": GKD_EMAIL,
        "password": GKD_PASSWORD
    })

    if r.json().get('m') == "操作成功":
        print("登录成功")
    else:
        send_message('登录失败', r.json())
        exit(1)


def submit(s: requests.Session):
    new_daily = {
        "number": GKD_NUMBER,
        "realname": GKD_NAME,

        # submitted date
        "date": time.strftime(r"%Y-%m-%d", time.localtime()),
        "jzdz": GEO_INFO[0],     # Residential Address
        "zrzsdd": "1",                       # Yesterday place to stay    1.雁栖湖  8.京外
        # Whether you are in school or not  1.是, 主要是在雁栖湖校区   5.否
        "sfzx": "1",
        "szgj": "中国",                       # current country
        "szdd": "国内",                       # current address
        "dqszdd": "1",                       # current location

        #
        "address": GEO_INFO[1]+GEO_INFO[2],
        "area": GEO_INFO[2],
        "province": GEO_INFO[1],
        "city": "",
        "geo_api_info": str({"address":GEO_INFO[1]+GEO_INFO[2],"details":GEO_INFO[3],"province":{"label":GEO_INFO[1],"value":""},"city":{"label":"","value":""},"area":{"label":GEO_INFO[2],"value":""}}),
        "szgj_api_info": "{\"area\":{\"label\":\"\",\"value\":\"\"},\"city\":{\"label\":\"\",\"value\":\"\"},\"address\":\"\",\"details\":\"\",\"province\":{\"label\":\"\",\"value\":\"\"}}",
        "szgj_select_info": {},
        #

        # whether you are in high or medium risk area or not  4. 无上述情况
        "dqsfzzgfxdq": "4",
        # do you have a travel history in risk area  4. 无上述情况
        "zgfxljs": "4",
        "tw": "1",                           # Today’s body temperature 1.37.2℃及以下
        # Do you have such symptoms as fever, fatigue, dry cough or difficulty in breathing today?
        "sffrzz": "0",
        "dqqk1": "1",                        # current situation      1.正常
        "dqqk1qt": "",
        "dqqk2": "1",                        # current situation      1.无异常
        "dqqk2qt": "",
        # 昨天是否接受核酸检测
        "sfjshsjc": "1",                     # PCR test?       1.是 0.否
        # 第一针接种
        "dyzymjzqk": "1",                    # first vaccination situation  1.已接种(科兴)
        "dyzjzsj": "2021-06-26",             # date of first vaccination
        "dyzwjzyy": "",
        # 第二针接种
        "dezymjzqk": "1",                    # second vaccination situation  1.已接种(科兴)
        "dezjzsj": "2021-07-23",             # date of second vaccination
        "dezwjzyy": "",
        # 第三针接种
        "dszymjzqk": "1",                    # third vaccination situation  1.已接种(科兴)
        "dszjzsj": "2022-01-27",             # default time
        "dszwjzyy": "",                      # reason of non-vaccination

        "gtshryjkzk": "1",                   # health situation
        "extinfo": "",                       # other information
        # personal information

        # "created_uid":"0",
        # "todaysfhsjc":"",
        # "is_daily":1,
        "geo_api_infot": str({"address":GEO_INFO[1]+GEO_INFO[2],"details":GEO_INFO[3],"province":{"label":GEO_INFO[1],"value":""},"city":{"label":"","value":""},"area":{"label":GEO_INFO[2],"value":""}}),

        # yesterday information
        "old_szdd": "国内",
        "old_city": str({"address":GEO_INFO_OLD[1]+GEO_INFO_OLD[2],"details":GEO_INFO_OLD[3],"province":{"label":GEO_INFO_OLD[1],"value":""},"city":{"label":"","value":""},"area":{"label":GEO_INFO_OLD[2],"value":""}}),
    }

    r = s.post("https://app.ucas.ac.cn/ucasncov/api/default/save", data=new_daily)
    print("提交信息:", new_daily)

    result = r.json()
    if result.get('m') == "操作成功":
        send_message('打卡成功', '打卡成功！地点为'+GEO_INFO[0])
    else:
        send_message('打卡失败', r.json().get("m"))


def send_message(title: str, content: str):
    print(title)
    print(content)
    res = requests.get(
        url='http://www.pushplus.plus/send',
        params={
            'token': PUSH_TOKEN,
            'title': title,
            'content': content
        }
    )
    if res.status_code != 200:
        print('推送失败: ' + res.text)


if __name__ == "__main__":
    try:
        login(s)
        submit(s)
    except Exception as e:
        send_message('执行错误', str(e))
