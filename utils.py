import os, json, datetime

def delete_folder_contents(folder_path):
    for file in os.listdir(folder_path):
        if '.gitignore' == file:
            continue
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  
            elif os.path.isdir(file_path):  
                os.rmdir(file_path)  
        except Exception as e:  
            print(f"Error deleting {file_path}: {e}")
    print("Assets cleaned")
    
def read_subjects():
    with open('subjects.txt') as file:
        return file.read().splitlines()

def delete_subject(subject):
    subjects = read_subjects()
    with open('subjects.txt', 'w') as file:
        for item in subjects:
            if item != subject:
                file.write(item+'\n')

def save_subjects(subjects: list):
    with open('subjects.txt', 'w') as file:
        for item in subjects:
            file.write(item+'\n')

def string_cutter(string:str,max:int):
    '''Cuts the string to have "max" number of chars'''
    while len(string) > max:
        string = string[:-2]
    if string[-1] == "#":
        string = string[:-2]
    return string

def parse_list_gpt(pseudo_list):
    if type(pseudo_list) == list:
        return pseudo_list
    else:
        fixed = pseudo_list.split(',')
        return fixed
    
def save_metadata(dict, file_name):
    with open(f'/tmp/assets/{file_name}.json', 'w') as f:
        json.dump(dict, f, indent = 6)

def load_metadata(file_name):
    with open(f'/tmp/assets/{file_name}.json') as f:
        return json.load(f)

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


def parse_time_to_now(time: tuple):
    parsed = datetime.datetime.now()

    if parsed.hour > time[0]:
        parsed += datetime.timedelta(days=1)

    parsed.replace(hour=time[0], minute=time[1])

    return parsed.year, parsed.month, parsed.day, parsed.hour, parsed.min

def youtube_upload(filename: str, title: str, desc: str, category: int, keywords: list, publishAt: tuple, privacy: str = "private",):

    year, month, day, hour, min = publishAt

    first = True
    for value in keywords:
        if first:
            keywords_str = value
            first = False
        else:
            keywords_str += ',' + value

    os.system(f'python3 uploaders/youtube_uploader.py --file "/tmp/result/{filename}.webm" \
              --title "{title}" \
              --description "{desc}" \
              --category {category} \
              --keywords "{keywords_str}" \
              --privacyStatus "{privacy}" \
              --publishAt "{convert_to_RFC_datetime(year, month, day, hour, min)}"')



