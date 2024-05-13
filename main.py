import os, re, subs, utils, random
import pexel
import uploaders.youtube_selenium as youtube_selenium
#from tiktok_uploader.upload import upload_video
import pandas as pd
from moviepy.editor import * # Taking my code months later I see that this is a really bad practice
from moviepy.video.tools.subtitles import SubtitlesClip

from llm.openai_utils import get_keywords, get_keywords_videos, get_description, get_script, get_subjects

from tiktokvoice import generate_tts

tiktok_session_id = os.environ['TIKTOK_SESSION_ID']

def get_tts(text, filename, voice='en_us_006'):
    generate_tts(text, voice, filename, False)

def parse_script_for_tts(script):
    parsed = []
    parsed = re.split("[.=!]",script)

    if parsed[-1] == '':
        parsed.pop(-1)
    #get rid of spaces
    i = 0
    for item in parsed:
        if item == ' ':
            parsed.pop(i)
            i += 1
            continue
        if parsed[i][0] == ' ':
            parsed[i]=parsed[i][1:]
        if parsed[i][-1] == ' ':
            parsed[i] = parsed[i][:-2]
        i += 1
    parsed.append('What do you think? Leave it in the comments and subscribe!')
    return parsed

def tts(file_name, script:str):
    p = parse_script_for_tts(script)
    print(p)
    i=0
    for s in p:
        if s != '':
            get_tts(s.replace('\n',''), f'/tmp/assets/{file_name}_script{i}.mp3')
            i+=1
    audio = []
    for i in range(len(p)):
        audio.append(AudioFileClip(f'/tmp/assets/{file_name}_script{i}.mp3'))
    #audio.pop(-1)
    final_audio = concatenate_audioclips(audio)

    #Si el audio es mas largo que un corto de youtube repito todo
    if final_audio.duration >= 60:
        return True

    
    final_audio.write_audiofile(f'/tmp/assets/{file_name}.mp3')
    return False

def get_videos(keywords:list):
    print(keywords)
    for keyword in keywords:
        vid = pexel.get_video_url(keyword)
        if vid != None:
            print(keyword)
            pexel.save_video(keyword, vid)



def pick_subject(cloud_run):
    subjects = utils.read_subjects()
    df = pd.DataFrame(subjects)
    print(df.to_string())
    if not cloud_run:
        select = int(input('Select subject index: '))
        return subjects[select]
    else:
        select = random.randint(0,len(df))
        return subjects[select]



def generate_video(file_name, cloud_run):    
    repeat = True
    repeat_same = False
    while repeat:
        if not repeat_same:
            if not cloud_run:
                input_subject = get_subjects()
                if input_subject:
                    subject = input('Input the subject you want: ')
                else:
                    subject = pick_subject()
            else:
                subject = pick_subject(cloud_run)
        

        script, video_name = get_script(subject)


        # Generate the tts
        repeat_same = tts(file_name, script)

        if repeat_same:
            print('TTS generated is larger than 60s, repeating...')
            continue

        # Look the keywords
        keywords = keywords = utils.parse_list_gpt(get_keywords_videos(subject))

        repeat_keywords = True
        while repeat_keywords:
            if len(keywords[0])==1 and len(keywords[1])==1:
                keywords = utils.parse_list_gpt(get_keywords_videos(subject))
            else:
                repeat_keywords = False

        # Get the videos
        get_videos(keywords)

        # get length of tts
        audio = AudioFileClip(f'/tmp/assets/{file_name}.mp3')
        duration = audio.duration
        video_duration = duration/len(keywords)

        # Load videos to one list
        videos = []
        extra_time = 0
        for keyword in keywords:
            try:
                videos.append(VideoFileClip('/tmp/assets/'+keyword+'.mp4'))
                videos[-1]=videos[-1].without_audio()
                videos[-1]=videos[-1].resize(width=1920)
                videos[-1]=videos[-1].crop(x_center = videos[-1].size[0]/2, y_center = videos[-1].size[1]/2, width = 607.5, height = 1080)
                if videos[-1].duration >= video_duration:
                    videos[-1]=videos[-1].subclip(0, video_duration)
                else:
                    extra_time += video_duration - videos[-1].duration
                    
            except Exception as e:
                print(f'Video with keyword {keyword} not found.', e)
        
        # Fill final video
        if extra_time > 0:
            for keyword in keywords:
                try:
                    videos.append(VideoFileClip('/tmp/assets/'+keyword+'.mp4'))
                    videos[-1]=videos[-1].without_audio()
                    videos[-1]=videos[-1].resize(width=1920)
                    videos[-1]=videos[-1].crop(x_center = videos[-1].size[0]/2, y_center = videos[-1].size[1]/2, width = 607.5, height = 1080)
                    if extra_time >= video_duration:
                        if videos[-1].duration < video_duration:
                            extra_time -= videos[-1].duration
                        else:
                            videos[-1]=videos[-1].subclip(0, video_duration)
                    else:
                        if videos[-1].duration < extra_time:
                            extra_time -= videos[-1].duration
                        else:
                            videos[-1]=videos[-1].subclip(0, extra_time)
                            break
                except Exception as e:
                    print(f'Video with keyword {keyword} not found for filling.', e)

        # ---------------------#
        # Merge videos and tts #
        # ---------------------#

        final = concatenate_videoclips(videos, method= 'compose')
        final = final.set_audio(audio)
        #final = final.crop(x_center = 1920/2, y_center = 1080/2, width = 607.5, height = 1080)

        # Add subtitles
        subs.get_str_file(file_name)
        generator = lambda txt: TextClip(txt, font='Impact', fontsize=32, color='white', stroke_color= 'black', stroke_width= 1, method='caption',size=final.size)
        sub_clip = SubtitlesClip('/tmp/assets/subs.srt', generator)
        final = CompositeVideoClip([final, sub_clip])

        # Output file
        print('---------------------------------------------------\nBuilding short final file\n---------------------------------------------------')
        #final.save_frame('snippet.png', t=5)
        #final.write_videofile('short.mp4', fps=24)
        final.write_videofile(f'/tmp/result/{file_name}.webm', bitrate = '50000k',fps=24, codec='libvpx', logger=None, threads=8, verbose='bar', preset='ultrafast')

        # Ask if want to repeat, scrap video or upload
        # but first preview the video
        #print('Escape to exit the preview and continue the process')
        #final.preview()
        # clean assets
        for video in videos:
            video.close()
        
        # Generate metadata for video if uploaded
        video_description = get_description(script)
        video_name = video_name + ' #facts #shorts #interestingfacts'
        video_name = utils.string_cutter(video_name, 100)
        tags = get_keywords(subject)
        print(f'--------------------{file_name}-----------------------')
        print(f'Name: {video_name}')
        print(f'Description: {video_description}')
        print(f'Tags: {tags}')
        defined_meta = {
            'subject': subject,
            'video_name': video_name,
            'video_description': video_description,
            'tags': tags,
                 }
        utils.save_metadata(defined_meta, file_name)
        if not cloud_run:
            select = input(f'Input "1" to upload video "{file_name}", "2" to scrap and repeat same, anything to scrap and pick another: ')
        else:
            select = '1'

        if select == '1':
            repeat = False
        elif select == '2':
            repeat = True
            repeat_same = True
        else:
            repeat = True
            repeat_same = False

def upload(file_name, schedule_time):

    # Parse time
    time = utils.parse_time_to_now(schedule_time)
    
    meta = utils.load_metadata(file_name)
    #youtube_selenium.upload_video(meta['video_name'], meta['video_description'], meta['tags'], file_name, schedule_time)
    utils.youtube_upload(file_name, meta['video_name'], meta['video_description'], 22, meta['tags'], time, "private")
    utils.delete_subject(meta['subject'])

    # TikTok upload
    # cookies_list = {
    # "domain": ".tiktok.com",
    # "expirationDate": 1704289252,
    # "name": "sessionid",
    # "path": "/",
    # "value": "3f6dfa6694e17b4fcc78a958c77ed021"
    #                 }
    
    # upload_video('short.webm', 
    #         description=video_description, 
    #         cookies_list=cookies_list)
        
    
def main():
    default_times = ((0,0), (7,0), (16,0)) # tuples that define  (hour, min)
    #quantity_of_videos = int(input('How many videos? '))
    
    tmp_dir = os.listdir('/tmp')

    if 'assets' not in tmp_dir:
        os.mkdir('/tmp/assets')
        
    if 'result' not in tmp_dir:
        os.mkdir('/tmp/result')
    
    # ask for times or use default ones
    for i in range(len(default_times)):

        utils.delete_folder_contents('/tmp/assets/')
        utils.delete_folder_contents('/tmp/result/')
        generate_video(f'short{i}')
        upload(f'short{i}', default_times[i%3])
        
    utils.delete_folder_contents('/tmp/assets/')
    utils.delete_folder_contents('/tmp/result/')

if __name__ == '__main__':
    main()