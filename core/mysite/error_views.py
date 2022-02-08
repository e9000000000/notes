from django.http import JsonResponse

def handler404(request, *args, **kwargs):
    response = JsonResponse({"detail": "not found"})
    response.status_code = 404
    return response

def handler500(request, *args, **kwargs):
    response = JsonResponse({"detail": "server error"})
    response.status_code = 500
    return response
