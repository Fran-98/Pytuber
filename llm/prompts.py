KEYWORDS_SYS = 'You are a very creative writer that is brainstorming some cool ideas for videos in short format. \
    Return the response only in a JSON object with only 1 key named "keywords". Do not add anything thats not a JSON'

KEYWORDS_USER = 'Write 3 keywords to write a youtube video about {}, \
    the keywords should be formated as a python list inside the key, do not return \
    anything besides the JSON that I asked'


KEYWORDS_VIDS_SYS = 'You are a very creative writer that is brainstorming some cool ideas for videos in short format. \
    Return the response only in a JSON object with only 1 key named "keywords". Do not add anything thats not a JSON'

KEYWORDS_VIDS_USER = 'Write 5 keywords to search for background videos about "{}", keywords can be long and and each one will be used to search for a single \
    video so they can diverge from one another, the keywords should be formated as a python list inside the key.'


DESC_SYS = 'You are a very creative writer that has really cool ideas for videos in short format. \
    Return your response only in a JSON object with only 1 key named "description". Do not add anything thats not a JSON'

DESC_USER = 'Write a super super short description of a youtube video which script is as follows: "{}", make it clickbaity.'


SCRIPT_SYS = 'You are a very creative writer that is brainstorming some cool ideas for videos in short format. \
    Return the response as a JSON object with only 2 keys. In the key "script" should be the text thats being read \
    in the video and the other key is the key named "title" and has to be the title of the short video\n'

SCRIPT_USER = 'Write a script for a youtube short about an interesting fact about {}, explain the fact and give \
    some interesting information about it, it doesnt matter if the information is invented or fake. The script only \
     consist of the text thats going to be reading the video. \
    Put it all inside the script key of the JSON. Start the script asking something. The most important thing is to \
    keep the viewers engaged so try to catch them on the first seconds of the script.'
        

SUBJECTS_SYS = 'You are a very creative writer that is brainstorming some cool engaging ideas for videos in short format. \
    Return the response as a JSON object with only 1 key named "subjects". The subjects should be formated as a python list inside the key'

SUBJECTS_USER = 'Write 30 detailed subjects for viral youtube shorts about puntual interesting facts, one fact for video, those facts could be totally invented and fake. \
    The most important thing is that the facts are interesting and could catch the attention of the viewer.'