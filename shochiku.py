import os
import re
import requests
from bs4 import BeautifulSoup
import urllib.parse
import hashlib

# 定义URL模板
url_template = "https://www.shochiku.co.jp/cinema/anime/{}/?showing=showing-end&y={}"

# 创建文件夹以保存图片
folder_name = "shochiku.co.jp"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# 定义正则表达式模式
image_pattern = re.compile(r'(-scaled|-\d{3}x\d{4}|-[\d]{4}x[\d]{4})')
theme_pattern = re.compile(r'https://www.shochiku.co.jp/wp-content/themes/')
 
import time

# 获取当前年份
current_year = time.localtime().tm_year

# 定义起始年份
start_year = 2016

# 根据当前年份动态设置结束年份
end_year = current_year + 1  # 结束年份是当前年份加1

# 创建从2016到当前年份加1的年份范围
years = range(start_year, end_year)
 
# 生成从2016到2024的所有自然数
print(years)
# 生成新的URL列表
new_urls = [url_template.format("lineup", "{}".format(year_start)) for year_start in years]
new_urls += [url_template.format("tv", "{}".format(year_start)) for year_start in years]
print(new_urls)
urls= [
   "https://www.shochiku.co.jp/cinema/anime/tv/",
   "https://www.shochiku.co.jp/cinema/anime/tv/?showing=showing-before",
   "https://www.shochiku.co.jp/cinema/anime/tv/?showing=showing-end",
   "https://www.shochiku.co.jp/cinema/anime/lineup/",
   "https://www.shochiku.co.jp/cinema/anime/lineup/?showing=showing-before",
   "https://www.shochiku.co.jp/cinema/anime/lineup/?showing=showing-end"
]
new_urls = urls + new_urls
print(new_urls)

# 定义一个函数来计算文件的MD5值
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# 遍历所有URL
for url in new_urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    img_srcs = [img.get('src') for img in img_tags]
    seen = set()
    img_srcs = [x for x in img_srcs if not (x in seen or seen.add(x))]

    # 下载并保存图片
    for img_src in img_srcs:
        img_src = urllib.parse.unquote(img_src)
        if img_src and not theme_pattern.search(img_src):
            # 使用正则表达式修改图片链接
            clean_img_src = re.sub(image_pattern, '', img_src)
            # 获取图片文件名
            image_name = clean_img_src.split("/")[-1]
            # 图片的完整路径
            image_path = os.path.join(folder_name, image_name)

            # 检查文件是否已存在
            if os.path.exists(image_path):
                # 计算已存在文件的MD5
                existing_md5 = calculate_md5(image_path)
                # 下载新文件并计算MD5
                new_md5 = hashlib.md5(requests.get(clean_img_src).content).hexdigest()
                # 如果MD5不同，则重命名新文件
                if existing_md5 != new_md5:
                    new_image_path = image_path + '.1'
                    with open(new_image_path, 'wb') as f:
                        f.write(requests.get(clean_img_src).content)
                    print(f"图片 {image_name}.1 已保存。")
                else:
                    print(f"……图片 {image_name} 已存在且相同，跳过下载。")
            else:
                # 下载图片
                with open(image_path, 'wb') as f:
                    f.write(requests.get(clean_img_src).content)
                print(f"图片 {image_name} 已保存。")

print("所有图片下载完成。")
