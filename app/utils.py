from googleapiclient.discovery import build
from django.conf import settings
import requests
from isodate import parse_duration

# api_key = config('YOUTUBE_API_KEY')

def get_authenticated_service():
    youtube = build('youtube', 'v3', developerKey=settings.MY_API_KEY)
    return youtube




