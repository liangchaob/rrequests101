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


# 获得目标作品的网站, github 地址,浏览量,好评数,所有评价
# 下载目标作品的全部截图
# 建立目标作品文件夹,把目标作品的相关参数写个文件存到该文件夹下,并把对应截图也放到该文件夹下

URL_F = 'https://fullstack.xinshengdaxue.com/'


# 获取目标页面的地址列表
def getUrlist(url):
    r = requests.get(url)
    e_html = etree.HTML(r.text)
    url_list = e_html.xpath('//div[@class="work-card-block"]/div[@class="img-block"]/a/@href')
    for n,item in enumerate(url_list):
        url_list[n] = URL_F + item
    return url_list



# 下载图片
def downloadImg(url,name,dir):
    img_file = requests.get(url, stream=True)
    with open(dir+'/'+name + '.jpg', 'wb') as f:
        for chunk in img_file.iter_content():
            f.write(chunk)



# 获得目标作品的网站, github 地址,好评数,图片地址列表
def projectInfo(url):
    r = requests.get(url)
    e_html = etree.HTML(r.text)
    heroku_url = e_html.xpath('//p[@class="heroku-url"]/a/@href')
    github_url = e_html.xpath('//p[@class="github-url"]/a/@href')
    img_url = e_html.xpath('//*[@id="mobile-width"]/img/@src')
    json_obj = {
        'heroku_url':heroku_url[0],
        'github_url':github_url[0],
        'img_url':img_url
    }
    return json_obj



# 主函数
def main():
    url_f = 'https://fullstack.xinshengdaxue.com/competitions/1/list_all?page='
    url_e = '&selection=order_by_vote'

    all_project=[]
    for n in xrange(3):
        url = url_f + str(n+1) + url_e
        # 获取地址列表
        url_list = getUrlist(url)
        all_project.extend(url_list)

    try:
        # 建立总文件夹
        os.mkdir('projects')

        # 建立各项目文件夹
        for n,i in enumerate(all_project):
            project_dir='projects/'+str(n)
            os.mkdir(project_dir)

            # 获取所有项目信息
            all_info = projectInfo(i)

            # 建立一个 readme 文件,写入项目信息
            with open(project_dir+'/readme.md','a') as readme:
                w = '项目地址:{heroku_url}\ngithub:{github_url}'
                w = w.format(heroku_url=all_info['heroku_url'],github_url=all_info['github_url'])
                readme.write(w)
            

            # 获得该项目下所有图片地址列表
            img_list = all_info.get('img_url')
            # 在该文件夹下下载所有当前项目文件
            for n,i in enumerate(img_list):
                # 下载图片
                downloadImg(i,str(n),project_dir)

    except Exception as e:
        pass



if __name__ == '__main__':
    main()


