from django.shortcuts import render

# Create your views here.
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.http import HttpResponse, JsonResponse

# Other dependency
import json

# Youtube dependency
# from pytube import YouTube
import pafy
from urllib import request
from datetime import datetime


def index(request):
    # print(list(get_files(StaticFilesStorage(), location='static')))
    #print("[Log ] index-temp_fetchVaccCenter_redirect: ",temp_fetchVaccCenter_redirect({"postData": "645"}))
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


def temp_fetchVaccCenter_redirect(jsonrequest):

    # if request.method == 'POST':
    if jsonrequest != {}:

        #ourid = request.POST["postData"]
        ourid = jsonrequest["postData"]

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection":	"keep-alive",
            "DNT":	"1",
            "TE": "Trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}

        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=%s&date=%s" % (
            ourid, datetime.today().strftime("%d-%m-%Y"))

        req = request.Request(url, None, headers)
        data = json.loads(request.urlopen(req).read())

        return JsonHttpResponse(data)

    else:

        html = '<p>This is not ajax</p>'
        return JsonResponse({{'data': {'msg': "Error"}}})


# def Downloader():
#     url = YouTube(str(link.get()))
#     video = url.streams.first()
#     video.download()
