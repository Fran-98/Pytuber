# youtube upload api
from youtube_upload.client import YoutubeUploader

def upload_video(video_name, video_description, tags:list):
    uploader = YoutubeUploader()

    uploader.authenticate()


    # Video options
    options = {
        "title" : video_name, # The video title
        "description" :video_description, # The video description
        "tags" : tags,
        "categoryId" : "22",
        "privacyStatus" : "public", # Video privacy. Can either be "public", "private", or "unlisted"
        "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
        # "thumbnailLink" : "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg" # Optional. Specifies video thumbnail.
    }

    # upload video
    uploader.upload('short.mp4', options) 

    #uploader.close()