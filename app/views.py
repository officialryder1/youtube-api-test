from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from django.conf import settings
import requests
from isodate  import parse_duration


api_key = settings.MY_API_KEY


def home(request):
    category = Category.objects.all()
    
    context = {
        'category':category
    }
    return render(request, 'core_app/index.html', context)


# Create your views here.

def search(request, name):
    videos = list()
    query = ''
    result = get_object_or_404(Category, name=name)
    

    # Search the api to find the video ids 
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    # After finding the ids use them to find more details about the videos
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    # the query from the search form
    query = result
    # If the search is empty the query will be
    # if query == '':
    #     query = 'Arsenal'
    
    # Param required for the youtube api
    search_params = {
        'part' : 'snippet',
        'q' : query,
        'safeSearch' : 'none',
        'maxResults' : 60,
        'key' : api_key,
        'type' : 'video',
    }

    response = requests.get(search_url, params=search_params)
    data = response.json()
    
    video_id = []
    for r in data['items']:
        video_id.append(r['id']['videoId'])

    # import random
    # random_num = random.randint(0,48)
    # # the request for 'lucky' the user is redirected to watch a random video from their search
    # if request.POST['submit'] == "lucky":
    #     return redirect(f'https://www.youtube.com/watch?v={video_id[random_num]}')
    #     # return redirect(f'searched_video,{video_id[random_num]}')
    
    # For videos
    video_params = {
        'key' : api_key,
        'part' : 'snippet,contentDetails',
        # create a string of ids separared by commas
        'id' : ','.join(video_id)
    }
    response = requests.get(video_url,params=video_params)
    data = response.json()
    
    for d in data['items']:
        video_data = {
            'title' : d['snippet']['title'],
            'time' : int(parse_duration(d['contentDetails']['duration']).total_seconds() // 60),
            'id' : d['id'],
            'thumbnail' : d['snippet']['thumbnails']['high']['url'],
            'url' : f'https://www.youtube.com/watch?v={d["id"]}',
        }

        videos.append(video_data)
    return render(request,'core_app/search.html', {'videos': videos,'query':query, 'result':result})


# For a single video and its details
def single_item(request,slug='name'):
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    
    
    params = {
        'key' : api_key,
        'part' : 'snippet,contentDetails',
        'id' : slug,
    }

    response = requests.get(video_url,params=params)
    data = response.json()

    video = {
        'id' : data['items'][0]['id'],
        'title' : data['items'][0]['snippet']['title'],
        'publishedAt' : data['items'][0]['snippet']['publishedAt'],
        'description' : data['items'][0]['snippet']['description'],
        'channelTitle' : data['items'][0]['snippet']['channelTitle'],
        'definition' : data['items'][0]['contentDetails']['definition'],
        'time' : int(parse_duration(data['items'][0]['contentDetails']['duration']).total_seconds() // 60),
        'url' : f'https://www.youtube.com/embed/{data["items"][0]["id"]}'
    }
    # print(data['items'][0]['snippet']['description'])
    return render(request,'core_app/detail.html',{'video':video})

