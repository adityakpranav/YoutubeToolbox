from django.shortcuts import render

# Create your views here.
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.http import HttpResponse, JsonResponse

# Other dependency
import json

# Youtube dependency
#from pytube import YouTube
import pafy


def index(request):
    # print(list(get_files(StaticFilesStorage(), location='static')))
    return render(request, 'Downloader/index.html')


def fetchVideo(request):

    if request.is_ajax() and request.method == 'POST':

        ourid = request.POST["postData"]
        return JsonHttpResponse(fetchVideoURL(ourid))

    else:

        html = '<p>This is not ajax</p>'
        return JsonResponse({{'data': {'msg': "Error"}}})


def JsonHttpResponse(jsonData):

    response_data = {}
    response_data['result'] = 'success'
    response_data['data'] = jsonData
    response_data["Content-Type"] = "application/octet-stream"
    # 'filename="download.mp4"'
    response_data['Content-Disposition'] = 'attachment; filename="download.mp4"'

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def yt_details(url):
    ytb = YouTube(url)
    data = {'data': {
            'msg': "OK",
            'title': ytb.title,
            'views': ytb.length,
            'length': ytb.length,
            'description': ytb.description,
            'rating': ytb.rating
            }
            }
    return(data)


def fetchVideoURL(url):
    video = pafy.new(url)

    videostreams = video.videostreams
    audiostreams = video.audiostreams

    video_data_name_url_dict = {}
    audio_data_name_url_dict = {}

    # video urls
    for i in range(len(videostreams)):
        video_data_name_url_dict[str(
            videostreams[i]).split("@")[-1]] = videostreams[i].url_https

    # audio urls
    for i in range(len(audiostreams)):
        audio_data_name_url_dict[str(
            audiostreams[i]).split("@")[-1]] = audiostreams[i].url_https

    payload = {"title": video.title,
               "time": video.duration,
               "author": video.author,
               "Vdata": video_data_name_url_dict,
               "Adata": audio_data_name_url_dict
               }

    return(payload)

    # print(fetchVideoURL("https://www.youtube.com/watch?v=e1IyzVyrLSU"))


# def Downloader():
#     url = YouTube(str(link.get()))
#     video = url.streams.first()
#     video.download()
