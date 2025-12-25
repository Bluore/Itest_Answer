import os
import json
from bs4 import BeautifulSoup

questions: list = []
directory = "questions"
data: dict
bank_quesInfos = []
res_quesInfos = []

def Html_to_Text(html: str):
    soup = BeautifulSoup(html, 'lxml')
    return soup.get_text()

def dealOneGroup():
    times = 0
    for oneQuesInfo in bank_quesInfos:
        if oneQuesInfo['quesTypeChName'] == '新闻报道（选择）_客观题':
            dealOneQuesInfo_listen(oneQuesInfo['subQuesInfos'])
        elif oneQuesInfo['quesTypeChName'] == '长对话_客观题':
            dealOneQuesInfo_listen(oneQuesInfo['subQuesInfos'])
        elif oneQuesInfo['quesTypeChName'] == '短文理解_客观题':
            dealOneQuesInfo_listen(oneQuesInfo['subQuesInfos'])
        elif oneQuesInfo['quesTypeChName'] == '词汇选择_客观题':
            dealOneQuesInfo_word(oneQuesInfo)
        elif oneQuesInfo['quesTypeChName'] == '长篇阅读_客观题':
            dealOneQuesInfo_math(oneQuesInfo)
        elif oneQuesInfo['quesTypeChName'] == '仔细阅读_客观题':
            dealOneQuesInfo_read(oneQuesInfo)
        elif oneQuesInfo['quesTypeChName'] == '句子翻译-英译汉-选择题_客观题':
            dealOneQuesInfo_translate(oneQuesInfo)
        elif oneQuesInfo['quesTypeChName'] == '写作_主观题机评':
            dealOneQuesInfo_write(oneQuesInfo)
        times += 1


def dealOneQuesInfo_listen(subQuesInfos: list):
    for queOne in subQuesInfos:
        questionOne: dict = {
            "type": "listen",
            "title": queOne['qtitle'],
            "answer":"",
            "options": [],
            "text": queOne['qtitle'],
            "audio": queOne['resPath']
        }
        print(queOne)
        for option in queOne['originalOptions']:
            if option['right']:
                questionOne['answer'] += option['optionValue']
            questionOne['options'].append(option['optionValue'])
            questionOne['text'] += '\n' + option['optionValue']
        questions.append(questionOne)

def dealOneQuesInfo_word(subQue: list):
    questionOne: dict = {
        "type": "word",
        "title": subQue['qtitle'],
        "answer": "",
        "options": [],
        "text": subQue['qtitle']
    }
    for option in subQue['originalOptions']:
        if option['right']:
            questionOne['answer'] += option['optionValue']
            questionOne_word: dict = {
                "type": "word",
                "title": subQue['qtitle'],
                "answer": questionOne['answer'],
                "options": [questionOne['answer']],
                "text": subQue['qtitle']
            }
            questions.append(questionOne_word)
        questionOne['options'].append(option['optionValue'])
        questionOne['text'] += '\n' + option['optionValue']
    questions.append(questionOne)

def dealOneQuesInfo_math(subQuesInfos: list):
    ansList: list = []
    for queOne in subQuesInfos['subQuesInfos']:
        questionOne: dict = {
            "type": "match",
            "title": queOne['qtitle'],
            "answer":queOne['qanswer']+"\n"+queOne['qtitle'],
            "options": [queOne['qanswer']],
            "text": Html_to_Text(queOne['qtitle'])
        }
        ansList.append(queOne['qanswer'])
        questions.append(questionOne)
    questionOne: dict = {
        "type": "match_text",
        "title": subQuesInfos['qtitle'],
        "answer": str(ansList),
        "options": ansList,
        "text": Html_to_Text(subQuesInfos['qtitle'])
    }
    questions.append(questionOne)

def dealOneQuesInfo_read(subQuesInfos: list):
    ansList: list = []
    for queOne in subQuesInfos['subQuesInfos']:
        questionOne: dict = {
            "type": "read",
            "title": queOne['qtitle'],
            "answer": "",
            "options": [],
            "text": Html_to_Text(queOne['qtitle'])
        }
        for option in queOne['originalOptions']:
            if option['right']:
                questionOne['answer'] += option['optionValue']
                ansList.append(option['optionValue'])
            questionOne['options'].append(option['optionValue'])
            questionOne['text'] += '\n' + option['optionValue']
        questions.append(questionOne)
    questionOne: dict = {
        "type": "read",
        "title": subQuesInfos['qtitle'],
        "answer": str(ansList),
        "options": ansList,
        "text": Html_to_Text(subQuesInfos['qtitle'])
    }
    questions.append(questionOne)

def dealOneQuesInfo_translate(subQue: list):
    questionOne: dict = {
        "type": "translate",
        "title": subQue['qtitle'],
        "answer": "",
        "options": [],
        "text": ""
    }
    for option in subQue['originalOptions']:
        if option['right']:
            questionOne['answer'] += option['optionValue']
        questionOne['options'].append(option['optionValue'])
        questionOne['text'] += '\n' + option['optionValue']
    questions.append(questionOne)

def dealOneQuesInfo_write(subQue: list):
    questionOne: dict = {
        "type": "write",
        "title": subQue['qtitle'],
        "answer": Html_to_Text(subQue['qanswer']),
        "options": [],
        "text": Html_to_Text(subQue['qtitle'])
    }
    questions.append(questionOne)


for filename in os.listdir(directory):
    if not filename.endswith(".json"):
        continue
    with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
        data = json.load(f)
    for quesGroups in data['rs']['quesGroups']:
        bank_quesInfos = quesGroups['quesInfos']
        res_quesInfos = quesGroups['questions']
        dealOneGroup()

with open("decode.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)