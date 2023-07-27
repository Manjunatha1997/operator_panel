from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
import json
from rest_framework.permissions import AllowAny
from operators.utils import Encoder, get_redis_image_util
from django.http import HttpResponse,StreamingHttpResponse




@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def start_process_view(request):
    data = json.loads(request.body)
    from operators.utils import start_process_util
    response,status_code = start_process_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def end_process_view(request):
    data = json.loads(request.body)
    from operators.utils import end_process_util
    response,status_code = end_process_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_running_process_view(request):
    from operators.utils import get_running_process_util
    response,status_code = get_running_process_util()
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
    
    
@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_metrics_view(request,inspection_id):
    from operators.utils import get_metrics_util
    response,status_code = get_metrics_util(inspection_id)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json") 




@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
def get_redis_image(request, key):
    from operators.utils import get_redis_image_util
    return StreamingHttpResponse(get_redis_image_util(key), content_type='multipart/x-mixed-replace; boundary=frame')


    
@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_all_parts_view(request):
    from operators.utils import get_all_parts_util
    response,status_code = get_all_parts_util()
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_mega_report_view(request):
    data = json.loads(request.body)
    from operators.utils import get_mega_report_util
    response,status_code = get_mega_report_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json") 


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def save_inspection_details_view(request):
    data = request.data

    from operators.utils import save_inspection_details_util
    response,status_code = save_inspection_details_util(data)

    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json") 



@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def start_inspection_view(request):
    data = json.loads(request.body)
    from operators.utils import start_inspection_util
    response,status_code = start_inspection_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
    
    
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def set_confidence(request):
    data = json.loads(request.body)
    from operators.utils import set_confidence_util
    response,status_code = set_confidence_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")