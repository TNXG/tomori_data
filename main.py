import os
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义数据目录
data_directory = 'data'
output_file = 'output.jsonl'

# 存储结果
messages = []

# 遍历数据目录下的所有文件
for filename in os.listdir(data_directory):
    if filename.endswith('.asset'):
        file_path = os.path.join(data_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            talk_data = data['Base']['talkData']
            
            # 提取对话
            for i in range(len(talk_data) - 1):
                user_body = talk_data[i]['body']
                assistant_body = talk_data[i + 1]['body'] if talk_data[i + 1]['windowDisplayName'] == '灯' else ''
                
                if assistant_body:
                    messages.append({
                        "messages": [
                            {"role": "user", "content": user_body},
                            {"role": "assistant", "content": assistant_body}
                        ]
                    })

# 保存到JSONL文件
with open(output_file, 'w', encoding='utf-8') as f:
    for message in messages:
        f.write(json.dumps(message, ensure_ascii=False) + '\n')
        logging.info(f"写入消息: {message}")

logging.info("数据处理完成，已保存至output.jsonl")
