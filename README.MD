# 从 bestdori 获取对话数据

更换

```python
assistant_body = talk_data[i + 1]['body'] if talk_data[i + 1]['windowDisplayName'] == '灯' else ''
```

可以获取其他服务器或者语言类型的数据集，获取一点小数据微调一下LLM