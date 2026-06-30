from django.http.response import JsonResponse
from django.shortcuts import render


# Create your views here.
def retrieve_info(request):
    """
    This view purpose is to return all data from RAG
    """
    return JsonResponse({}, safe=False)
