#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : test.py
# @Author   : jade
# @Date     : 2023/11/14 19:43
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from aligo import Aligo

if __name__ == '__main__':
    ali = Aligo()
    share_token = ali.get_share_token('hnWeeeNjbdq')
    file_list = ali.get_share_file_list(share_token)
    print(file_list[0].file_id,file_list[0].parent_file_id)
    share_file_list = ali.list_by_share(share_token, "6552f121a01865959eb143c490af2f6b9ace6b62")
    for share_file in share_file_list:
        share_url = ali.get_share_link_download_url(share_file.file_id,share_token)
        if share_url:
            print(share_url.download_url)

