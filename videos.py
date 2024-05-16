import requests, random, os

pexel_key = os.environ['PEXEL_KEY']
pixabay_key = os.environ['PIXABAY_KEY']

videos_per_page = 20
def get_video_url(query):
    # First try with pexel
    url = get_video_url_pexel(query)
    if url != None:
        return url
    url = get_video_url_pixabay(query)
    return url

def get_video_url_pexel(query,):
    url = f'https://api.pexels.com/videos/search?query={query}&per_page={videos_per_page}'
    headers = {
        'Authorization':pexel_key,
    }
    r = requests.get(headers=headers, url=url)
    # print(r)
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
    with open(f'/tmp/assets/{name}.mp4', "wb") as f: # opening a file handler to create new file 
        f.write(resp.content) # writing content to file


def get_video_url_pixabay(query: str,):
    url = f'https://pixabay.com/api/videos/?key={pixabay_key}&q={query.replace(" ","+")}&per_page={videos_per_page}'

    r = requests.get(url=url)
    # print(r)
    if r.status_code != 400:
        response = r.json()
        #print(response)
        if response['total'] > 0:
            repeat = True
            i = 0
            while repeat:
                videos = response['hits']
                selected_video = videos[random.randint(0,len(videos)-1)]['videos']
                if 'large' in selected_video:
                    video_url = selected_video['large']['url']
                elif 'medium' in selected_video:
                    video_url = selected_video['medium']['url']
                else:
                    video_url = None

                if video_url != None:
                    repeat = False
                i += 1
                if i > videos_per_page * 3:
                    return None
            return video_url
        
    return None

#print(get_video_url_pexel('nature'))
#print(get_video_url_pixabay('nature'))