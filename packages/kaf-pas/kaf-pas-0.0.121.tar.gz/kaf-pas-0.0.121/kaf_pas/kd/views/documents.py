import logging

import requests
from django.conf import settings
from django.http import HttpResponseRedirect

from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from isc_common.logger.Logger import Logger
from kaf_pas.kd.models.documents import Documents, DocumentManager

logger = logging.getLogger(__name__)
logger.__class__ = Logger


@JsonResponseWithException()
def Documents_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Documents.objects.
                select_related('attr_type').
                get_range_rows1(
                request=request,
                function=DocumentManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_Add(request):
    return JsonResponse(DSResponseAdd(data=Documents.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_Update(request):
    return JsonResponse(DSResponseUpdate(data=Documents.objects.updateFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_Remove(request):
    ws_channel = request.session.get('ws_channel')
    ws_port = settings.WS_PORT
    host = settings.WS_HOST

    _request = DSRequest(request=request)
    ids = _request.get_tuple_ids()
    r = requests.get(f'{settings.KOMPAS_INFORMICA}/logic/Documents/Remove', params=dict(ids=ids, port=ws_port, ws_channel=ws_channel, host=host, user_id=_request.user_id))
    HttpResponseRedirect(r.url)
    return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Documents.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_Info(request):
    return JsonResponse(DSResponse(request=request, data=Documents.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_MakeItem(request):
    from kaf_pas.ckk.models.attr_type import Attr_type
    from kaf_pas.kd.models.documents_ext import DocumentManagerExt

    _request = DSRequest(request=request)
    ids = _request.get_data()
    if isinstance(ids, dict):
        for id in ids.get('ids'):
            document = Documents.objects.get(id=id)
            if document.attr_type.code == 'SPW':

                DocumentManagerExt(logger=logger).make_spw(document=document, user=request.user)

            elif document.attr_type.code == 'CDW':
                DocumentManagerExt(logger=logger).make_cdw(document=document, user=request.user)

            elif document.attr_type.code == 'KD_PDF':

                STMP_1_type = Attr_type.objects.get(code='STMP_1')
                STMP_2_type = Attr_type.objects.get(code='STMP_2')

                DocumentManagerExt(logger=logger).make_pdf(document=document, STMP_1_type=STMP_1_type, STMP_2_type=STMP_2_type, user=request.user)
    return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Documents_Treat(request):
    ws_channel = request.session.get('ws_channel')
    ws_port = settings.WS_PORT
    host = settings.WS_HOST

    _request = DSRequest(request=request)
    ids = _request.get_tuple_ids()
    r = requests.get(f'{settings.KOMPAS_INFORMICA}/logic/Documents/Treat', params=dict(ids=ids, port=ws_port, ws_channel=ws_channel, host=host, user_id=_request.user_id))
    HttpResponseRedirect(r.url)
    return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response) @ JsonResponseWithException()


@JsonResponseWithException()
def Documents_ReloadDoc(request):
    ws_channel = request.session.get('ws_channel')
    ws_port = settings.WS_PORT
    host = settings.WS_HOST

    _request = DSRequest(request=request)
    ids = _request.json.get('data')
    ids = ids.get('ids')

    r = requests.get(f'{settings.KOMPAS_INFORMICA}/logic/Documents/ReloadDoc', params=dict(ids=ids, port=ws_port, ws_channel=ws_channel, host=host, user_id=_request.user_id))
    HttpResponseRedirect(r.url)
    return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response)
