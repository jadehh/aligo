#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : test.py
# @Author   : jade
# @Date     : 2023/11/14 19:43
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import time

from aligo import Aligo


import json
import requests

class Ali():

    def get_download_url(self):
        url = "https://open.aliyundrive.com/adrive/v1.0/openFile/getDownloadUrl"
        params = {"file_id": "6554339735f0f2ac9e3d4e5b8223d0ad89cb2be1", "drive_id": "303583582"}
        headers = {
            "Content-Type": "application/json",
            "authorization": "Bearer eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmMjBkYjViMmZmYzk0ZTA4YWRmZTA4Y2VlNzY5YmE3YSIsImF1ZCI6Ijc2OTE3Y2NjY2Q0NDQxYzM5NDU3YTA0ZjYwODRmYjJmIiwiaXNzIjoiaHR0cHM6Ly9vcGVuLmFsaXl1bmRyaXZlLmNvbSIsImV4cCI6MTcwMDAyMDg4NywiaWF0IjoxNzAwMDEzMDg3LCJqdGkiOiI1NTFiNzA2M2Y2ODI0MjM4YjliMzU2ZGNlMzA2YzFlYSJ9.U9Jii2I7i7LV4q-XXDnOMIA4OYiZH9c2NsXTeJDpFgo",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Referer": "https://www.aliyundrive.com/"}
        results = requests.post(url, timeout=60)
        print(results)

    def get_ali_logion(self):
        url = "https://auth.aliyundrive.com/v2/account/token"
        params = {
            "refresh_token": "c2ddc8d762a94880a6112065f8ff0512",
            "grant_type": "refresh_token"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url,json.dumps(params),headers=headers, timeout=60)
        if response.status_code != 200:
            print("阿里登录失败")
            self.get_ali_logion()
        else:
            return response.json()


    def get_alist_code(self,login_json):
        """
        通过Alist应用去访问阿里云盘
        """
        authorization = login_json['token_type'] + " " + login_json['access_token']
        url = "https://open.aliyundrive.com/oauth/users/authorize?client_id=76917ccccd4441c39457a04f6084fb2f&redirect_uri=https://alist.nn.ci/tool/aliyundrive/callback&scope=user:base,file:all:read,file:all:write&state="
        params = {"authorize": 1, "scope": "user:base,file:all:read,file:all:write"}
        headers = {'Content-Type':'application/json',"authorization": authorization}
        respose = requests.post(url, data=json.dumps(params),headers=headers, timeout=60)
        if respose.status_code != 200:
            print("获取Alist Code失败")
            self.get_alist_code(self.get_ali_logion())
        else:
            return (respose.json()["redirectUri"].split("code=")[-1])

    def get_access_token(self,code):
        """
        Access Token 有效期较短,需要重新获取 Access Token
        token只有三个小时有效期，三个小时到期后，需要重复获取
        access_token的作用是什么？
        access_token的作用主要是用于API的授权和认证。
        在API的使用过程中，访问令牌可以保证API的安全性，
        防止未授权的访问以及恶意攻击。
        例如，在一些需要身份验证的应用中，用户必须提供正确的访问令牌才能访问API。
        在这种情况下，access_token就成为了身份认证的一种方式。
        """
        url = "https://api.xhofe.top/alist/ali_open/code"
        params = {"code": code, "grant_type": "authorization_code"}
        response = requests.post(url, data=json.dumps(params),headers = {'Content-Type':'application/json'}, timeout=60)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print("Access Token获取失败")
            time.sleep(60)
            self.get_access_token(self.get_alist_code(self.get_ali_logion()))


if __name__ == '__main__':
    ali = Ali()
    login_result = ali.get_ali_logion()
    alist_code = ali.get_alist_code(login_result)
    access_token = ali.get_access_token(alist_code)
    access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmMjBkYjViMmZmYzk0ZTA4YWRmZTA4Y2VlNzY5YmE3YSIsImF1ZCI6Ijc2OTE3Y2NjY2Q0NDQxYzM5NDU3YTA0ZjYwODRmYjJmIiwiaXNzIjoiaHR0cHM6Ly9vcGVuLmFsaXl1bmRyaXZlLmNvbSIsImV4cCI6MTcwMDA1ODYwNiwiaWF0IjoxNzAwMDUwODA2LCJqdGkiOiJmNzZmNTUxOGNhZjk0ODliODBhNGFhODZkMDNmOThhZCJ9.-ayfwYfQqjXFnjO8rFssxyvGOozIqUogcl9MyYJKzg8"
    print(access_token,len(access_token))
    # ali = Aligo()
    # share_token = ali.get_share_token('hnWeeeNjbdq')
    # file_list = ali.get_share_file_list(share_token)
    # print(file_list[0].file_id,file_list[0].parent_file_id)
    # share_file_list = ali.list_by_share(share_token, "6552f121a01865959eb143c490af2f6b9ace6b62")
    # for share_file in share_file_list:
    #     share_url = ali.get_share_link_download_url(share_file.file_id,share_token)
    #     if share_url:
    #         print(share_url.download_url)

