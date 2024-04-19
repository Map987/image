import os
import re
import requests
from bs4 import BeautifulSoup

# sitemap URL
sitemap_url = 'http://cineport.jp/post-sitemap.xml'

# 下载图片的函数，同时处理URL
def download_image(image_url, save_folder, txt_file):
    # 删除URL中的"-scaled"和分辨率部分（如"-724x1024”），但只有当分辨率后缀后面没有其他字符时
    pattern = r'(-\d+x\d+)(?![\w-])'
    processed_url = re.sub(pattern, '', image_url)
    processed_url = re.sub('-scaled', '', processed_url)
    
    response = requests.get(processed_url)
    if response.status_code == 200:
        file_name = os.path.join(save_folder, processed_url.split('/')[-1])
        with open(file_name, 'wb') as f:
            f.write(response.content)
        file_size = os.path.getsize(file_name)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(txt_file, 'a') as tf:
            tf.write(f"{processed_url} | {file_size} bytes | {current_time}\n")
        print(f"Downloaded {processed_url} to {file_name} | Size: {file_size} bytes")
        return file_name, file_size, current_time
    else:
        print(f"Failed to download {processed_url}")
        return None, None, None

# 解析sitemap并下载图片
def parse_sitemap(sitemap_url, save_folder, txt_file):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, 'xml')
    urls = soup.find_all('url')
    for url in urls:
        loc_tag = url.find('loc')
        if loc_tag:
            post_url = loc_tag.text
            post_response = requests.get(post_url)
            post_soup = BeautifulSoup(post_response.text, 'html.parser')
            img_tag = post_soup.find('img', class_='attachment-post-thumbnail')
            if img_tag and 'srcset' in img_tag.attrs:
                srcset = img_tag['srcset']
                img_urls = srcset.split(', ')
                # Find the smallest image
                smallest_img_url = min(img_urls, key=lambda x: int(x.split(' ')[-2].replace('w', '')))[:-1]
                download_image(smallest_img_url, save_folder, txt_file)

# 主函数
import datetime

if __name__ == '__main__':
    save_folder = 'downloaded_images'
    txt_file = 'downloaded_images.txt'
    readme_file = 'README.md'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    if not os.path.exists(txt_file):
        with open(txt_file, 'w') as tf:
            tf.write("Image URL | File Size | Download Time\n")
    parse_sitemap(sitemap_url, save_folder, txt_file)

    # Update README.md
    with open(txt_file, 'r') as tf:
        lines = tf.readlines()
    with open(readme_file, 'r') as rf:
        readme_content = rf.readlines()
    # Insert the new downloads at the beginning of the README
    new_content = lines[1:] + readme_content
    with open(readme_file, 'w') as rf:
        rf.writelines(new_content)
