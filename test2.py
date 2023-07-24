import youtube_selenium

video_description = 'Test'
video_name = 'Test' + ' #facts #shorts #interestingfacts'
print('-------------------------------------------')
print(f'Name: {video_name}')
print(f'Description: {video_description}')
tags = ['testing']
print(f'Tags: {tags}')
#youtube_uploader.upload_video(video_name, video_description, tags)
youtube_selenium.upload_video(video_name, video_description, tags)
