import os
import requests
from bs4 import BeautifulSoup

# sitemap URL
sitemap_url = 'http://cineport.jp/post-sitemap.xml'

# 下载图片的函数
def download_image(image_url, save_folder):
    response = requests.get(image_url)
    if response.status_code == 200:
        file_name = os.path.join(save_folder, image_url.split('/')[-1])
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {image_url} to {file_name}")

# 解析sitemap并下载图片
def parse_sitemap(sitemap_url, save_folder):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, 'xml')
    urls = soup.find_all('url')
    for url in urls:
        image_tag = url.find('image:image')
        if image_tag:
            image_loc = image_tag.find('image:loc').text
            download_image(image_loc, save_folder)

# 主函数
if __name__ == '__main__':
    save_folder = 'downloaded_images'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    parse_sitemap(sitemap_url, save_folder)
