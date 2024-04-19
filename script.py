import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# sitemap URL
sitemap_url = 'http://cineport.jp/post-sitemap.xml'

# 处理下载原图URL的函数
def process_main_image_url(image_url):
    pattern = r'(-\d+x\d+)(?![\w-])'
    processed_url = re.sub(pattern, '', image_url)
    processed_url = re.sub('-scaled', '', processed_url)
    return processed_url

# 下载图片的函数
def download_image(image_url, save_folder, txt_file):
    response = requests.get(image_url)
    if response.status_code == 200:
        file_name = os.path.join(save_folder, image_url.split('/')[-1])
        with open(file_name, 'wb') as f:
            f.write(response.content)
        file_size = os.path.getsize(file_name)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(txt_file, 'a') as tf:
            tf.write(f"{image_url} | {file_size} bytes | {current_time}\n")
        print(f"Downloaded {image_url} to {file_name} | Size: {file_size} bytes")
        return file_name, file_size, current_time
    else:
        print(f"Failed to download {image_url}")
        return None, None, None

# 解析sitemap并下载图片
def parse_sitemap(sitemap_url, save_folder_main, save_folder_thumb, txt_file_main, txt_file_thumb):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, 'xml')
    urls = soup.find_all('url')
    for url in urls:
        # 下载<image:image>内的图片
        image_tag = url.find('image:image')
        if image_tag:
            image_loc = image_tag.find('image:loc').text
            processed_url = process_main_image_url(image_loc)
            download_image(processed_url, save_folder_main, txt_file_main)
        
        # 下载<img>标签的srcset属性中最小尺寸的图片
        loc_tag = url.find('loc')
        if loc_tag:
            post_url = loc_tag.text
            post_response = requests.get(post_url)
            post_soup = BeautifulSoup(post_response.text, 'html.parser')
            img_tag = post_soup.find('img', class_='attachment-post-thumbnail')
            if img_tag and 'srcset' in img_tag.attrs:
                srcset = img_tag['srcset']
                # 确保srcset中包含有效的尺寸信息
                if 'w' in srcset:
                    img_urls = re.findall(r'https?://\S+', srcset)
                    sizes = [int(re.search(r'(\d+)w', url).group(1)) for url in img_urls if re.search(r'(\d+)w', url)]
                    if sizes:
                        smallest_img_url = img_urls[sizes.index(min(sizes))]
                        download_image(smallest_img_url, save_folder_thumb, txt_file_thumb)


# 主函数
if __name__ == '__main__':
    save_folder_main = 'downloaded_images_main'
    save_folder_thumb = 'downloaded_images_thumb'
    txt_file_main = 'downloaded_images_main.txt'
    txt_file_thumb = 'downloaded_images_thumb.txt'
    
    if not os.path.exists(save_folder_main):
        os.makedirs(save_folder_main)
    if not os.path.exists(save_folder_thumb):
        os.makedirs(save_folder_thumb)
    
    if not os.path.exists(txt_file_main):
        with open(txt_file_main, 'w') as tf:
            tf.write("Image URL | File Size | Download Time\n")
    if not os.path.exists(txt_file_thumb):
        with open(txt_file_thumb, 'w') as tf:
            tf.write("Image URL | File Size | Download Time\n")
    
    parse_sitemap(sitemap_url, save_folder_main, save_folder_thumb, txt_file_main, txt_file_thumb)
