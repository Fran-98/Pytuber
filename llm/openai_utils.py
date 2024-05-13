from openai import OpenAI
from llm.prompts import (KEYWORDS_SYS, 
                     KEYWORDS_USER, 
                     KEYWORDS_VIDS_SYS, 
                     KEYWORDS_VIDS_USER,
                     DESC_SYS,
                     DESC_USER,
                     SCRIPT_SYS,
                     SCRIPT_USER,
                     SUBJECTS_SYS,
                     SUBJECTS_USER
                     )
import json
from utils import save_subjects

client = OpenAI()
model="gpt-3.5-turbo"
#model="gpt-4-turbo-preview"

def get_response(sys: str, user: str):
    completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": sys},
        {"role": "user", "content": user}
    ]
    )
    print(completion)
    return completion.choices[0].message.content


def get_keywords(subject):
    again = True
    while again:
        keywords_short = get_response(KEYWORDS_SYS, KEYWORDS_USER.format(subject))
        try:
            keywords_short = json.loads(keywords_short)
            again = False
            print(keywords_short)
            return keywords_short['keywords']
        except Exception as e:
            print(f'Error generating keywords {e}') #Only for debug reasons, it shouldn't have problems here
            again = True


def get_keywords_videos(subject):
    again = True
    while again:
        keywords_short = get_response(KEYWORDS_VIDS_SYS, KEYWORDS_VIDS_USER.format(subject))
        try:
            keywords_short = json.loads(keywords_short)
            again = False
            #print(keywords_short)
            return keywords_short['keywords']
        except Exception as e:
            print(f'Error generating keywords for videos {e}') #Only for debug reasons, it shouldn't have problems here
            again = True


def get_description(script):
    again = True
    while again:
        keywords_short = get_response(DESC_SYS, DESC_USER.format(script))
        try:
            keywords_short = json.loads(keywords_short)
            again = False
            return keywords_short['description']
        except Exception as e:
            print(f'Error generating description {e}') #Only for debug reasons, it shouldn't have problems here
            again = True


def get_script(subject):
    valid = False
    while not valid:
        r = get_response(SCRIPT_SYS, SCRIPT_USER.format(subject))
        try:
            dic = r.replace('\n','')
            dic = json.loads(dic)
            print(dic)
            script = dic['script'].replace('\n','')
            video_name = dic['title']
            valid = True
            return script, video_name
        except Exception as e:
            print(e)
            valid = False
    

def get_subjects():
    ask = input('"1" to generate subjects, "2" to input subject, or anything to use existent list: ')
    if ask == '1':
        again = True
        while again:
            subjects_short = get_response(SUBJECTS_SYS, SUBJECTS_USER)
            print(subjects_short)
            try:
                subjects_short = json.loads(subjects_short.replace('\n',''))
                again = False
                break
            except Exception as e:
                print(e)
                again = True
                
        save_subjects(subjects_short['subjects'])
        return False
    if ask == '2':
        return True

# get_keywords('LLMs')