import json
import uuid

from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render

from upload.backend import extract_summary_from_media_file
from upload.forms import MediaFileForm
from upload.models import MediaFile


def home(request):
    form = MediaFileForm()

    context = {"form": form}

    if request.method == 'POST':
        received_form = MediaFileForm(request.POST, request.FILES)
        media_object = received_form.save()
        context["unique_id"] = str(media_object.unique_id)

    all_media_objects = MediaFile.objects.all()
    context.update({"all_files": all_media_objects})
    return render(request, "upload.html", context)


def run(request):
    if request.is_ajax() and request.method == 'POST':
        data = request.POST
        try:
            id_data: str = data["unique_id"]
            id_data = id_data.replace("-", "")
            unique_id = uuid.UUID(id_data)
        except ValueError as exc:
            unique_id = None
            print(exc)
        media_file_objects = MediaFile.objects.filter(unique_id=unique_id)
        if media_file_objects.exists():
            media_file_object: MediaFile = media_file_objects.first()
            if media_file_object.summary == "":
                url = media_file_object.file.url
                try:
                    summary, question_list, compression_ratio = extract_summary_from_media_file(url)
                    media_file_object.summary = summary
                    media_file_object.questions = json.dumps(question_list)
                    media_file_object.compression_ratio = compression_ratio
                    media_file_object.save()
                    final_list = json.dumps(question_list)
                except Exception as exc:
                    return JsonResponse({
                        "has_error": True
                    })
            else:
                summary = media_file_object.summary
                final_list = media_file_object.questions
                compression_ratio = media_file_object.compression_ratio

            # Returning JSON Response
            return JsonResponse({
                "summary": summary,
                "question_list": final_list,
                "compression_ratio": compression_ratio,
                "has_error": False
            })
        else:
            return JsonResponse({
                "has_error": True
            })

    return HttpResponseNotFound("Page not found")
