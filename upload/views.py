from django.shortcuts import render

from upload.forms import MediaFileForm


def home(request):
    form = MediaFileForm()
    if request.method == 'GET':
        return render(request, "upload.html", {"form": form})
    else:
        received_form = MediaFileForm(request.POST, request.FILES)
        received_form.save()
        return render(request, "upload.html", {"form": form})
