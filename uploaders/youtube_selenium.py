from youtube_uploader_selenium import YouTubeUploader
import json



def upload_video(video_name, video_description, tags:list, file_name, schedule_time:str):

    options = {
        "title" : video_name, # The video title
        "description" :video_description, # The video description
        "tags" : tags,
        "categoryId" : "22",
        "privacyStatus" : "public", # Video privacy. Can either be "public", "private", or "unlisted"
        "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
        # "thumbnailLink" : "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg" # Optional. Specifies video thumbnail.
    }
    metadata_path = 'metadata.json'
    with open(metadata_path,'w') as file:
        json.dump(options,file)
    
    #video_path = 'short.mp4'
    video_path = f'result/{file_name}.webm'

    uploader = YouTubeUploader(video_path, metadata_path)
    #schedule = input('"1" To schedule, whatever to public now: ') 
    schedule = '1'
    if schedule == '1':
        was_video_uploaded = uploader.upload(schedule_time, True)
    else:
        was_video_uploaded = uploader.upload(schedule_time, False)
    assert was_video_uploaded
