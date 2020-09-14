from django.shortcuts import render
from upload.forms import MediaFileForm
from upload.models import MediaFile
from upload.backend import backend


def home(request):
    form = MediaFileForm()
    # get url for the video file from s3
    # obj: MediaFile = MediaFile.objects.all().first()
    # url = obj.photo.url
    # run the backend function
    # backend(url)                            #remove this comment symbol

    if request.method == 'GET':
        return render(request, "upload.html", {"form": form})
    else:
        received_form = MediaFileForm(request.POST, request.FILES)
        received_form.save()
        return render(request, "upload.html", {"form": form})
