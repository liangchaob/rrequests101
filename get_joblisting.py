#!/usr/bin/env python
# encoding: utf-8
'''
* liangchaob@163.com 
* 2017.2
'''
#设置中文字符
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import os
import requests
from lxml import etree

# 获取当前页面的所有图片地址列表
def getImg(url):
    r = requests.get(url)
    e_html = etree.HTML(r.text)
    img_list = e_html.xpath('//div[@class="work-card-block"]/div[@class="img-block"]/a/img/@src')
    return img_list

# 下载图片
def downloadImg(url,name,dir):
    img_file = requests.get(url, stream=True)
    with open(dir+'/'+name + '.jpg', 'wb') as f:
        for chunk in img_file.iter_content():
            f.write(chunk)

# 主函数
def main():
    url_f = 'https://fullstack.xinshengdaxue.com/competitions/1/list_all?page='
    url_e = '&selection=order_by_vote'
    all_img=[]
    for n in xrange(3):
        url = url_f + str(n+1) + url_e
        # 获取地址列表
        img_list = getImg(url)
        all_img.extend(img_list)
    # 建立图片文件夹
    os.mkdir('projects')
    for s,i in enumerate(all_img):
        # 下载图片
        downloadImg(i,str(s),'projects')


if __name__ == '__main__':
    main()