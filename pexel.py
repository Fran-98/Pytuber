import requests, json
pexel_key = 'kKrad2pwpu5LylJ1OlTMwm28U9VekaEt4l77PHqV9zvZVO1ltkipKZSK'

def get_video_url(query,):
    url = f'https://api.pexels.com/videos/search?query={query}&per_page=1'
    headers = {
        'Authorization':pexel_key,
    }
    r = requests.get(headers=headers, url=url)
    print(r)
    if r.status_code != 400:
        response = r.json()
        print(response)
        if response['total_results'] > 0:
            video_url = get_hd_video(response['videos'][0]['video_files'])
            return video_url
        
    return None
    

def get_hd_video(videos):
    for video in videos:
        if video['quality'] == 'hd':
            return video['link']
    return videos[0]['link']

def save_video(name:str, url:str):
    resp = requests.get(url) # making requests to server
    with open('assets/'+name+'.mp4', "wb") as f: # opening a file handler to create new file 
        f.write(resp.content) # writing content to file
