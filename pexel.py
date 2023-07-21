import requests, json, random, os
pexel_key = os.environ['PEXEL_KEY']

videos_per_page = 10

def get_video_url(query,):
    url = f'https://api.pexels.com/videos/search?query={query}&per_page={videos_per_page}'
    headers = {
        'Authorization':pexel_key,
    }
    r = requests.get(headers=headers, url=url)
    print(r)
    if r.status_code != 400:
        response = r.json()
        #print(response)
        if response['total_results'] > 0:
            repeat = True
            i = 0
            while repeat:
                if response['total_results'] >= videos_per_page:
                    video_url = get_hd_video(response['videos'][random.randint(0,videos_per_page-1)]['video_files'])
                    if video_url != None:
                        repeat = False
                else:
                    video_url = get_hd_video(response['videos'][random.randint(0,response['total_results']-1)]['video_files'])
                    if video_url != None:
                        repeat = False
                i += 1
                if i > videos_per_page * 3:
                    return None
            return video_url
        
    return None
    

def get_hd_video(videos):
    for video in videos:
        if video['quality'] == 'hd' and video['width'] == 1920:
            return video['link']
    return None

def save_video(name:str, url:str):
    resp = requests.get(url) # making requests to server
    with open('assets/'+name+'.mp4', "wb") as f: # opening a file handler to create new file 
        f.write(resp.content) # writing content to file

#print(get_video_url('sun'))