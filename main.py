import os, json, re, subs, utils, threading, random
import pexel
import youtube_uploader
import youtube_selenium
from tiktok_uploader.upload import upload_video
import pandas as pd
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import gpt4free.GPT as gpt

tiktok_session_id = '3f6dfa6694e17b4fcc78a958c77ed021'

def get_tts(text, filename, voice='en_us_006'):
    os.system(f'python tts.py -v {voice} -t "{text}" -n {filename} --session {tiktok_session_id}')

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
            get_tts(s.replace('\n',''), f'assets/{file_name}_script{i}.mp3')
            i+=1
    audio = []
    for i in range(len(p)):
        audio.append(AudioFileClip(f'assets/{file_name}_script{i}.mp3'))
    #audio.pop(-1)
    final_audio = concatenate_audioclips(audio)

    #Si el audio es mas largo que un corto de youtube repito todo
    if final_audio.duration >= 60:
        return True

    
    final_audio.write_audiofile(f'assets/{file_name}.mp3')
    return False

def get_videos(keywords:list):
    print(keywords)
    for keyword in keywords:
        vid = pexel.get_video_url(keyword)
        if vid != None:
            print(keyword)
            pexel.save_video(keyword, vid)

def get_keywords(subject):
    again = True
    while again:
        keywords_short = gpt.get_response(f'return the response in JSON format with only 1 key named "keywords", this key contains 3 keywords to put in a title of a youtube video about {subject}, the keywords should be formated as a python list inside the key, do not return anything besides the JSON that I asked')
        try:
            keywords_short = json.loads(keywords_short)
            again = False
            break
        except:
            again = True
    return keywords_short['keywords']

def get_keywords_videos(subject):
    again = True
    while again:
        keywords_short = gpt.get_response(f'return the response in JSON format with only 1 key named "keywords", this key contains 5 keywords to search for the background videos about "{subject}", keywords can be long and each one will be used to search for a single video, the keywords should be formated as a python list inside the key, do not return anything besides the JSON that I asked')
        try:
            keywords_short = json.loads(keywords_short)
            again = False
            break
        except:
            again = True
    return keywords_short['keywords']

def get_description(script):
    again = True
    while again:
        desc = gpt.get_response(f'return the response in JSON format with only 1 key named "description", this key contains a super short description of a youtube video which script is : "{script}"')
        try:
            desc = json.loads(desc)
            again = False
            break
        except:
            again = True
    return desc['description']

def pick_subject():
    subjects = utils.read_subjects()
    df = pd.DataFrame(subjects)
    print(df.to_string())
    select = int(input('Select subject index: '))
    #select = random.randint(0,len(df))
    return subjects[select]

def generate_subjects():
    ask = input('"1" to generate subjects, "2" to input subject, or anything to use existent list: ')
    if ask == '1':
        again = True
        while again:
            subjects_short = gpt.get_response(f'return the response in JSON format with only 1 key named "subjects", this key contains 100 detailed subjects for viral youtube shorts about puntual interesting facts, one fact for video, the subjects should be formated as a python list inside the key')
            try:
                subjects_short = json.loads(subjects_short.replace('\n',''))
                again = False
                break
            except:
                again = True
                
        utils.save_subjects(subjects_short['subjects'])
        return False
    if ask == '2':
        return True

def generate_video(file_name):    
    repeat = True
    repeat_same = False
    while repeat:
        # Get prompt and make it a dict
        formatting_prompt = 'Temperature:1. Return the response as a JSON object with only 2 keys. In the key "script" should be the text thats being read in the video and the other key is the key named "title" and has to be the title of the short video\n'
        
        if not repeat_same:
            input_subject = generate_subjects()
            if input_subject:
                subject = input('Input the subject you want: ')
            else:
                subject = pick_subject()
        
        valid = False
        while not valid:
            r = gpt.get_response(formatting_prompt + f'Write a script for a youtube short about one interesting fact about {subject}, explain the fact and give some interesting information about it. The script only consist of the text thats going to be reading the video. Put it all inside the script key of the JSON. Start the script asking something.')
            try:
                dic = r.replace('\n','')
                dic = json.loads(dic)
                print(dic)
                script = dic['script'].replace('\n','')
                video_name = dic['title']
                valid = True
            except:
                valid = False

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
        audio = AudioFileClip(f'assets/{file_name}.mp3')
        duration = audio.duration
        video_duration = duration/len(keywords)

        # Load videos to one list
        videos = []
        extra_time = 0
        for keyword in keywords:
            try:
                videos.append(VideoFileClip('assets/'+keyword+'.mp4'))
                videos[-1]=videos[-1].without_audio()
                videos[-1]=videos[-1].resize(width=1920)
                videos[-1]=videos[-1].crop(x_center = videos[-1].size[0]/2, y_center = videos[-1].size[1]/2, width = 607.5, height = 1080)
                if videos[-1].duration >= video_duration:
                    videos[-1]=videos[-1].subclip(0, video_duration)
                else:
                    extra_time += video_duration - videos[-1].duration
                    
            except:
                print(f'Video with keyword {keyword} not found.')
        
        # Fill final video
        if extra_time > 0:
            for keyword in keywords:
                try:
                    videos.append(VideoFileClip('assets/'+keyword+'.mp4'))
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
                except:
                    print(f'Video with keyword {keyword} not found.')

        # Merge videos and tts

        final = concatenate_videoclips(videos, method= 'compose')
        final = final.set_audio(audio)
        #final = final.crop(x_center = 1920/2, y_center = 1080/2, width = 607.5, height = 1080)

        # Add subtitles
        subs.get_str_file(file_name)
        generator = lambda txt: TextClip(txt, font='Impact', fontsize=32, color='white', stroke_color= 'black', stroke_width= 1, method='caption',size=final.size)
        sub_clip = SubtitlesClip('assets/subs.srt', generator)
        final = CompositeVideoClip([final, sub_clip])

        # Output file
        print('---------------------------------------------------\nBuilding short final file\n---------------------------------------------------')
        #final.save_frame('snippet.png', t=5)
        #final.write_videofile('short.mp4', fps=24)
        final.write_videofile(f'result/{file_name}.webm', bitrate = '50000k',fps=24, codec='libvpx', logger=None, threads=8)

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
        jason = {
            'subject': subject,
            'video_name': video_name,
            'video_description': video_description,
            'tags': tags,
                 }
        utils.save_metadata(jason, file_name)
        select = input(f'Input "1" to upload video "{file_name}", "2" to scrap and repeat same, anything to scrap and pick another: ')
        if select == '1':
            repeat = False
        elif select == '2':
            repeat = True
            repeat_same = True
        else:
            repeat = True
            repeat_same = False

def upload(file_name, schedule_time):
    
    meta = utils.load_metadata(file_name)
    #youtube_uploader.upload_video(video_name, video_description, tags)
    youtube_selenium.upload_video(meta['video_name'], meta['video_description'], meta['tags'], file_name, schedule_time)
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
    default_times = ('0:00', '7:00', '16:00')
    #quantity_of_videos = int(input('How many videos? '))
    
    # ask for times or use default ones
    for i in range(len(default_times)):
        
        generate_video(f'short{i}')
        upload(f'short{i}', default_times[i%3])
        
    utils.delete_folder_contents('assets/')
    utils.delete_folder_contents('result/')

main()