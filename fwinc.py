 
import os
import requests
from bs4 import BeautifulSoup
import re
import json
import html

# 获取nonce的函数
def get_nonce(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script', type='text/javascript')
        nonce_pattern = re.compile(r'nonce":\s*"([^"]+)"')
        for script in script_tags:
            if script.string and 'nonce' in script.string:
                nonce_match = nonce_pattern.search(script.string)
                if nonce_match:
                    return nonce_match.group(1)
    return None

# 下载图片的函数
def download_images(image_urls, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for image_url in image_urls:
        filename = os.path.join(folder, image_url.split('/')[-1])
        with requests.get(image_url, stream=True) as r:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

# 目标网页URL
animation_url = 'https://www.fwinc.co.jp/animation/'

# 获取nonce
nonce = get_nonce(animation_url)
if nonce:
    # 构建请求URL
    request_url = f'https://www.fwinc.co.jp/wp-admin/admin-ajax.php?action=animation_ajax_handler&nonce={nonce}'
    
    # 发送请求
    response = requests.get(request_url)
    ree = requests.get(animation_url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON数据
        data = json.loads(response.text)
        
        # 检查是否成功并提取image链接
        if data.get('success'):
            # 解码Unicode字符并删除特定关键词
            image_pattern = re.compile(r'(-scaled|-\d{3}x\d{4}|-[\d]{4}x[\d]{4})')
            image_urls = [image_pattern.sub('', html.unescape(item['image'])) for item in data['data']]
            
            # 下载图片
            download_images(image_urls, 'fwinc.co.jp')
            
            # 获取img src的图片链接
            soup = BeautifulSoup(ree.text, 'html.parser')
            img_tags = soup.find_all('img')
            img_srcs = [img.get('src') for img in img_tags]
            img_srcs = [url for url in img_srcs if re.match(r'http', url)]
            print(img_srcs)
            # 下载img src的图片
            download_images(img_srcs, 'fwinc.co.jp')
        else:
            print('Failed to retrieve data.')
    else:
        print(f'Failed to retrieve data: Status code {response.status_code}')
else:
    print('Failed to retrieve nonce.')
