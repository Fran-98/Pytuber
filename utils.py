import os

def delete_folder_contents(folder_path):
    for file in os.listdir(folder_path):
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