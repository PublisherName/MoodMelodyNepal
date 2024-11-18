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
    expression = getExpression(uri)
    return JsonResponse({"mood": expression})
