import uploaders.youtube_selenium as youtube_selenium
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from tiktok_uploader.upload import upload_video

cookies_list = {
        "domain": ".tiktok.com",
        "expirationDate": 1704289252,
        "name": "sessionid",
        "path": "/",
        "value": "3f6dfa6694e17b4fcc78a958c77ed021"
                        }
        
upload_video('short.webm', 
        description='Test', 
        cookies_list=cookies_list)