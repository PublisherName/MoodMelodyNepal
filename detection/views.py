import base64
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from detection.detect import getExpression


def index(request):
    return render(request, "index.html")


@csrf_exempt  # allows the function to return a HTTP response... django problem
def expression(request):
    uri = json.loads(request.body)["image_uri"]
    mood, jpeg_bytes = getExpression(uri)
    jpeg_base64 = base64.b64encode(jpeg_bytes).decode("utf-8")
    return JsonResponse({"mood": mood, "image": jpeg_base64})
