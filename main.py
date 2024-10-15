import os
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义数据目录和输出文件
data_directory = 'data'
output_file = 'output.json'  # 可改为 'output.json' 来测试不同格式

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

# 根据输出文件的扩展名保存数据
if output_file.endswith('.json'):
    new_format_data = []
    for msg in messages:
        new_format_data.append({
            "instruction": msg['messages'][0]['content'],
            "input": "",
            "output": msg['messages'][1]['content'],
            "history": []
        })
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_format_data, f, ensure_ascii=False, indent=4)
        logging.info(f"写入消息至新的 JSON 格式文件: {output_file}")
else:  # 默认处理为 jsonl
    with open(output_file, 'w', encoding='utf-8') as f:
        for message in messages:
            f.write(json.dumps(message, ensure_ascii=False) + '\n')
            logging.info(f"写入消息: {message}")

logging.info("数据处理完成，已保存至" + output_file)