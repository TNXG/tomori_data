import os
import re
import aiohttp
import asyncio

def read_bundle_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def find_matches(content):
    pattern = re.compile(r'"assets/star/forassetbundle/(?:startapp|asneeded)/(.*?)"')
    return pattern.findall(content)

async def async_download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    
    # 检查文件是否已经存在
    if os.path.exists(local_filename):
        print(f"文件已存在，跳过下载: {local_filename}")
        return local_filename
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
    return local_filename

async def main():
    directory = './'  # 当前目录
    dest_folder = 'bundle_data'  # 下载文件保存的目录
    
    bundle_files = [f for f in os.listdir(directory) if f.endswith('.bundle')]
    
    if not bundle_files:
        print("未找到任何 .bundle 文件。")
        return
    
    tasks = []
    for bundle_file in bundle_files:
        bundle_path = os.path.join(directory, bundle_file)
        print(f"处理文件: {bundle_path}")
        
        content = read_bundle_file(bundle_path)
        matches = find_matches(content)
        
        if matches:
            print("匹配到的字段:")
            for match in matches:
                print(match)
                parts = match.split('/')
                if len(parts) >= 2:
                    collection = parts[-2]
                    filename = parts[-1].capitalize()
                    if 'event' in collection:
                        url = f"https://bestdori.com/assets/cn/scenario/eventstory/{collection}_rip/{filename}"
                    else:
                        url = f"https://bestdori.com/assets/cn/scenario/{collection}_rip/{filename}"
                    print(f"正在下载: {url}")
                    tasks.append(async_download_file(url, dest_folder))
            print(f"文件 {bundle_file} 下载完成。")
        else:
            print(f"文件 {bundle_file} 未匹配到任何字段。")
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()