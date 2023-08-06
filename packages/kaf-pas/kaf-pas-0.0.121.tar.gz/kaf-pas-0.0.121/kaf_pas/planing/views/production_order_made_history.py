from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.production_order_made_history import Production_order_made_history, Production_order_made_historyManager


@JsonResponseWithException()
def Production_order_made_history_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Production_order_made_history.objects.
                select_related('executor').
                get_range_rows1(
                request=request,
                function=Production_order_made_historyManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_Add(request):
    return JsonResponse(DSResponseAdd(data=Production_order_made_history.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_Update(request):
    return JsonResponse(DSResponseUpdate(data=Production_order_made_history.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_Info(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
