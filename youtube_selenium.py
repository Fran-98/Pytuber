from youtube_uploader_selenium import YouTubeUploader
import json



def upload_video(video_name, video_description, tags:list):

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
    video_path = 'short.webm'

    uploader = YouTubeUploader(video_path, metadata_path)
    was_video_uploaded = uploader.upload()
    assert was_video_uploaded
