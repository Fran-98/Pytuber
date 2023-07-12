from . import g4f

from .g4f.Provider import (
    Ails,
    You,
    Bing,
    Yqcloud,
    Theb,
    Aichat,
    Bard,
    Vercel,
    Forefront,
    Lockchat,
    Liaobots,
    H2o,
    ChatgptLogin,
    DeepAi,
    GetGpt
) 


providers = (
    DeepAi,
    GetGpt,
    Ails,
    You,
    Bing,
    Theb,
    Yqcloud,
    Vercel,
    Forefront,
    Aichat,
    Bard,
    Lockchat,
    Liaobots,
    H2o,
    ChatgptLogin,
) 


def clean_response(response:str):
    clean = response
    chars_to_clean = ['[',']','(',')',':']
    for char in chars_to_clean:
        clean = clean.replace(char,'')
    clean = clean.split('\n')
    return clean

def save_txt(str):
    with open('script.txt', 'w') as f:
        f.write(str)
    
def get_response(prompt):
    i = 0
    responded = False
    while not responded:
        #print(i)
        try:
            r = g4f.ChatCompletion.create(model=g4f.models.Model.gpt_35_turbo, provider=providers[i],messages=[{"role": "user", "content": prompt}]) # alterative model 
            if r == '':
                raise 'null value'
        except:
            i += 1
        else:
            if 'The webpage has been updated. Please refresh the page and try again.' in r:
                i += 1
            elif '17690845214' in r:
                i += 1
            elif 'Vercel is currently not working.' in r:
                i += 1
            elif 'gpt@binjie.site' in r:
                i += 1
            else:
                break
    return r


# normal response
# "Create an script for a youtube short about an interesting fact, do not explain what you are doing only give me the text, put the word 'Narrator' at the start of the sentense read by the narrator and 'effects' for the effects"
#prompt = "Do not explain anything you do, do not say anything besides what I ask you to give me, make the text, only the text, for a youtube short video about an interesting fact, do not put what cuts should be, do not say wich lines are for the narrator, write the text in one single block"
#response = get_response(prompt)

#save_txt(response)

