import os, json, datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scope)
drive = GoogleDrive(gauth)

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


def read_file(title_file, id_file):
    """
    Function to read txt files from google drive
    """
    metadata = dict(id = id_file)

    google_file = drive.CreateFile(metadata = metadata)

    google_file.GetContentFile(filename = f"/tmp/{title_file}.txt")

    content_bytes = google_file.content ; # BytesIO

    string_data = content_bytes.read().decode( 'utf-8' )

    return string_data


def read_subjects():
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    for file in file_list:
        if "subjects" in file['title']:
            #print(file['title'])
            return read_file(file['title'], file['id']).splitlines()

    # If no subject exist, create one

    return None

def delete_subjects_files():
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    for file in file_list:
        #print(file)
        if "subjects" in file['title']:
            drive.CreateFile({'id': file['id']}).Delete()


def find_subjects_file():
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    for file in file_list:
        #print(file)
        if "subjects" in file['title']:
            return file['id']
    
    # If not found a file return None and manage that case
    return None

def upload_subject(items: str):
    subject_id = find_subjects_file()
    if subject_id:
        file1 = drive.CreateFile({'title': 'subjects.txt', 'id': subject_id})
    else:
        file1 = drive.CreateFile({'title': 'subjects.txt'}) # Create new file

    file1.SetContentString(items)
    file1.Upload() # Files.insert()

def delete_subject(subject):
    subjects = read_subjects()
    items = ''
    for item in subjects:
        if item != subject:
            items += item+'\n'
    
    upload_subject(items)
            

def save_subjects(subjects: list):
    items = ''
    for item in subjects:
        items += item+'\n'
    upload_subject(items)


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

    parsed = parsed.replace(hour=time[0], minute=time[1])
    return parsed.year, parsed.month, parsed.day, parsed.hour, parsed.minute

def youtube_upload(filename: str, title: str, desc: str, category: int, keywords: list, publishAt: tuple, privacy: str = "private",):

    year, month, day, hour, min = publishAt

    first = True
    for value in keywords:
        if first:
            keywords_str = value
            first = False
        else:
            keywords_str += ',' + value
    
    # args = {
    #     "file": f"/tmp/result/{filename}.webm",
    #     "title": title,
    #     "description": desc,
    #     "category": category,
    #     "keywords": keywords_str,
    #     "privacyStatus": privacy,
    #     "publishAt": convert_to_RFC_datetime(year, month, day, hour, min)
    # }

    os.system(f'python uploaders/youtube_uploader.py --file "/tmp/result/{filename}.webm" \
              --title "{title}" \
              --description "{desc}" \
              --category {category} \
              --keywords "{keywords_str}" \
              --privacyStatus "{privacy}" \
              --publishAt "{convert_to_RFC_datetime(year, month, day, hour, min)}"')



