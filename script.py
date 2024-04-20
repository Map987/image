import os
import requests
from bs4 import BeautifulSoup

# 下载图片的函数
def download_image(image_url, save_folder):
    response = requests.get(image_url)
    if response.status_code == 200:
        file_name = os.path.join(save_folder, image_url.split('/')[-1])
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {image_url} to {file_name}")
    else:
        print(f"Failed to download {image_url}")

# 主函数
if __name__ == '__main__':
    save_folder = 'test_images'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # 指定的图片URL
    image_url = "https://cdn.aqdstatic.com:966/age/20240045.jpg"
    
    # 下载图片
    download_image(image_url, save_folder)
