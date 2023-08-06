import requests
from django.conf import settings
from django.http import HttpResponseRedirect

from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.kd.models.pathes import Pathes
from kaf_pas.kd.models.pathes_view import Pathes_view, Pathes_viewManager


@JsonResponseWithException()
def Pathes_view_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Pathes_view.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Pathes_viewManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Pathes_view_Add(request):
    return JsonResponse(DSResponseAdd(data=Pathes.objects.createFromRequest(request=request, propsArr=['enable_upload']), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Pathes_view_Update(request):
    return JsonResponse(DSResponseUpdate(data=Pathes.objects.updateFromRequest(request=request, propsArr=['enable_upload']), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Pathes_view_Remove(request):
    ws_channel = request.session.get('ws_channel')
    ws_port = settings.WS_PORT
    host = settings.WS_HOST

    _request = DSRequest(request=request)
    ids = _request.get_tuple_ids()
    r = requests.get(f'{settings.KOMPAS_INFORMICA}/logic/Pathes/Remove', params=dict(ids=ids, port=ws_port, ws_channel=ws_channel, host=host, user_id=_request.user_id))
    HttpResponseRedirect(r.url)
    return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Pathes_view_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Pathes_view.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Pathes_view_Info(request):
    return JsonResponse(DSResponse(request=request, data=Pathes_view.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)
