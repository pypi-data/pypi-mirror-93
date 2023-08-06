from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.production_order_tmp import Production_order_tmp, Production_order_tmpManager


@JsonResponseWithException()
def Production_order_tmp_Fetch(request):
    _request = DSRequest(request)
    return JsonResponse(
        DSResponse(
            request=request,
            data=Production_order_tmp.objects.
                select_related('opertype', 'creator', 'status', 'launch', 'item').
                get_range_rows1(
                request=request,
                function=Production_order_tmpManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_tmp_Add(request):
    return JsonResponse(DSResponseAdd(data=Production_order_tmp.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_tmp_Update(request):
    return JsonResponse(DSResponseUpdate(data=Production_order_tmp.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_tmp_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_tmp.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_tmp_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_tmp.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_tmp_Info(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_tmp.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_tmp_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_tmp.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_tmp_Count(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_tmp.objects.get_queryset().get_Count(request=request), status=RPCResponseConstant.statusSuccess).response)

@JsonResponseWithException()
def Production_order_tmp_Check(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_tmp.objects.get_queryset().get_Check(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_tmp_SetCount(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_tmp.objects.get_queryset().set_Count(request=request), status=RPCResponseConstant.statusSuccess).response)
