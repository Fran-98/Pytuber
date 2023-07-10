import datetime
import time
from googleapiclient.http import MediaFileUpload
import pandas as pd
from google_apis import create_service

API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']
# SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
client_file = 'client-secret.json'


#service = create_service(client_file, API_NAME, API_VERSION, SCOPES)

def video_categories():
    video_categories = service.videoCategories().list(part='snippet', regionCode='US').execute()
    df = pd.DataFrame(video_categories.get('items'))
    return pd.concat([df['id'], df['snippet'].apply(pd.Series)[['title']]], axis=1)

def upload_video(video_name, video_description, tags:list):
    #print(video_categories())

    """
    Step 1. Uplaod Video
    """
    service = create_service(client_file, API_NAME, API_VERSION, SCOPES)
    upload_time = (datetime.datetime.now() + datetime.timedelta(days=0)).isoformat() + '.000Z'

    request_body = {
        'snippet': {
            'title': video_name,
            'description': video_description,
            'categoryId': 27,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'public',
            'publishedAt': upload_time,
            'selfDeclaredMadeForKids': False
        },
        'notifySubscribers': False
    }

    video_file = 'short.mp4'
    media_file = MediaFileUpload(video_file)
    # print(media_file.size() / pow(1024, 2), 'mb')
    # print(media_file.to_json())
    # print(media_file.mimetype())

    response_video_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()
    uploaded_video_id = response_video_upload.get('id')


    """
    Step 2. Update video thumbnail
    """
    # response_thumbnail_upload = service.thumbnails().set(
    #     videoId=uploaded_video_id,
    #     media_body=MediaFileUpload('assets/thumbnail.png')).execute()