 
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 要访问的网页URL列表及其备注
urls = [
    ('https://arifureta.com/bluray/4318', '#bd1'),
    ('https://arifureta.com/bluray/4420', '#bd2'),
    ('https://arifureta.com/bluray/4301', '#news里的bd2'),
    ('https://arifureta.com/bluray/4438', '#bd3'),
    ('https://arifureta.com/bluray/4323', '#news里的bd3'),
    ('https://arifureta.com/bluray/4440', '#bd4'),
    ('https://arifureta.com/bluray/4329', '#news里的bd4')
]

# 确保下载文件夹存在
download_folder = 'arifureta.com'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# 遍历URL列表
for url, note in urls:
    # 发送HTTP请求
    response = requests.get(url)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有的<img>标签
        img_tags = soup.find_all('img')
        
        # 提取并下载每个<img>标签的src属性
        for img in img_tags:
            # 获取图片的完整URL
            img_url = urljoin(url, img['src'])
            
            # 移除"-scaled"关键词
            img_url = img_url.replace('-scaled', '')
            
            # 获取图片的文件名
            img_filename = os.path.basename(img_url)
            
            # 下载图片
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                # 保存图片到文件夹
                with open(os.path.join(download_folder, img_filename), 'wb') as f:
                    f.write(img_response.content)
                print(f"Downloaded {img_filename} {note}")
            else:
                print(f"Failed to download {img_url}, status code: {img_response.status_code}")
    else:
        print(f"Request failed for {url}, status code: {response.status_code}")
