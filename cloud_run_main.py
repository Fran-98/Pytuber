import os
from main import generate_video, upload

def cloud_run_pipeline():
    default_times = ((9,0), (16,0)) # tuples that define  (hour, min)
    #quantity_of_videos = int(input('How many videos? '))
    
    tmp_dir = os.listdir('/tmp')

    if 'assets' not in tmp_dir:
        os.mkdir('/tmp/assets')
        
    if 'result' not in tmp_dir:
        os.mkdir('/tmp/result')
    
    # ask for times or use default ones
    for i in range(len(default_times)):

        generate_video(f'short{i}', True)
        upload(f'short{i}', default_times[i%3])

if __name__ == "__main__":
    cloud_run_pipeline()