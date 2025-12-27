#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取 decode.json 题库，生成 Rime 输入法词典 iTest_answer_dict.txt
新格式：首字母（小写） 答案（仅保留字母）
首字母提取规则：将 text 字段按行分割，取每行第一个字母（忽略空格），连接后转为小写。
"""

import json
import re

def keep_letters_only(text):
    """只保留大小写英文字母，去除其他所有字符"""
    return re.sub(r'[^A-Za-z]', '', text)

def extract_initials(text):
    """
    从 text 中提取每行的首字母，连接并转为小写。
    每行去除前后空白，取第一个字母字符（若没有字母则取第一个字符）。
    """
    lines = text.split('\n')
    initials = []
    for line in lines:
        flag:bool = True
        for i in line :
            if i.isalpha():
                if flag:
                    initials.append(i.lower())
                    flag = False
            else:
                flag = True

        # line = line.strip()
        # if not line:
        #     continue
        # # 查找第一个字母字符
        # match = re.search(r'[A-Za-z]', line)
        # if match:
        #     first_letter = match.group(0)
        # else:
        #     first_letter = line[0] if line else ''
        # initials.append(first_letter)
    return ''.join(initials).lower()

def main():
    input_file = 'decode.json'
    output_file = 'iTest_answer_dict.txt'

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lines = []
    for item in data:
        answer = item.get('answer', '').strip()
        if not answer:
            continue

        text = item.get('text', '').strip()
        if not text:
            continue

        initials = keep_letters_only(extract_initials(text))
        cleaned_answer = keep_letters_only(answer)

        # Rime 格式：答案 首字母（制表符分隔）
        line = f"{initials[:5]},1={cleaned_answer}"
        lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"生成完成，共 {len(lines)} 条词条，已写入 {output_file}")

if __name__ == '__main__':
    main()