# Itest_Answer 导出工具

这是一个用于处理抓包得到的 `question/1-1.json` 等文件的项目，能够将原始数据导出为格式化的 JSON 文件，并进一步生成交互式网页以供复习。

格式化后的 JSON 文件结构清晰，便于其他程序读取；生成的网页则方便复习查看题目和答案。

## 文件结构

```
.
├── decode_question.py          # 主处理脚本，将原始 JSON 转换为格式化 JSON
├── output_HTML.py              # 将格式化 JSON 转换为 HTML 网页
├── output_rime-table.py        # 将格式化 JSON 导出为 Rime 输入法词库
├── decode.json                 # 格式化后的题目数据（由 decode_question.py 生成）
├── quiz.html                   # 生成的网页（由 output_HTML.py 生成）
├── iTest_answer_dict.txt       # Rime 词库文件（由 output_rime-table.py 生成）
├── questions/                  # 原始抓包数据（.json 文件）
│   ├── 1-1.json
│   ├── 1-2.json
│   └── ...
└── README.md                   # 项目说明
```

## 使用方法

### 1. 环境准备

确保已安装 Python 3.x 以及以下依赖库：

- `beautifulsoup4`
- `lxml`

可以通过以下命令安装：

```bash
pip install beautifulsoup4 lxml
```

### 2. 运行数据解析

将抓包得到的 JSON 文件放入 `questions/` 目录（默认已存在一些示例文件），然后运行：

```bash
python decode_question.py
```

该脚本会读取 `questions/` 下的所有 `.json` 文件，合并处理并生成 `decode.json`。

### 3. 生成网页

在得到 `decode.json` 后，运行：

```bash
python output_HTML.py
```

脚本会读取 `decode.json` 并生成 `quiz.html`。用浏览器打开该文件即可浏览所有题目。

### 4. 导出为Rime词库

如果你希望将题库转换为 [Rime](https://rime.im/) 输入法的词库文件，可以使用 `output_rime-table.py` 脚本。

首先确保已生成 `decode.json`，然后运行：

```bash
python output_rime-table.py
```

脚本会读取 `decode.json`，提取每道题目的文本首字母作为编码，答案作为词条，生成 `iTest_answer_dict.txt` 文件。该文件符合 Rime 词库格式，可直接用于 Rime 输入法。

## 数据格式说明

`decode.json` 是一个 JSON 数组，每个元素代表一道题目，结构如下：

```json
{
  "type": "listen",
  "title": "What is the heated discussion about?",
  "answer": "Arrangements for digital legacy.",
  "options": [
    "Rules of digital games.",
    "Plans for digital revolution.",
    "Arrangements for digital legacy.",
    "Laws on digital privacy protection."
  ],
  "text": "...",
  "audio": null
}
```

- `type`：题目类型，如 `listen`（听力）、`read`（阅读）、`match`（匹配）、`translate`（翻译）、`write`（写作）等。
- `title`：题干（可能包含 HTML 标签）。
- `answer`：正确答案。
- `options`：选项列表（选择题）。
- `text`：纯文本形式的题目内容（已去除 HTML 标签）。
- `audio`：音频资源路径（如有）。

## Rime词库格式

`iTest_answer_dict.txt` 是一个纯文本文件，每行包含一个词条，格式为：

```
答案	编码
```

其中：
- **答案**：题目的正确答案（仅保留英文字母，去除空格和标点）。
- **编码**：由题目文本每行的首字母组成的小写字符串（仅保留字母）。

例如，若题目文本为：
```
What is the heated discussion about?
Arrangements for digital legacy.
```
则提取的首字母为 `wa`（每行第一个字母 `W` 和 `A` 的小写），答案经过清洗后为 `Arrangementsfordigitallegacy`，因此词条为：

```
Arrangementsfordigitallegacy	wa
```

该文件可直接导入 Rime 输入法使用。

## 示例

项目已附带示例数据，运行后可直接查看效果。

1. 执行 `python decode_question.py` 生成 `decode.json`。
2. 执行 `python output_HTML.py` 生成 `quiz.html`。
3. 执行 `python output_rime-table.py` 生成 `iTest_answer_dict.txt`（Rime 词库文件）。
4. 用浏览器打开 `quiz.html`，即可看到所有题目，点击“显示答案”按钮查看答案。

## 注意

**本项目仅供学习交流使用，请勿用于非法用途**

