from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.production_order_made_history_operations import Production_order_made_history_operations, Production_order_made_history_operationsManager


@JsonResponseWithException()
def Production_order_made_history_operations_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Production_order_made_history_operations.objects.
                select_related().
                get_range_rows1(
                request=request,
                function=Production_order_made_history_operationsManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_operations_Add(request):
    return JsonResponse(DSResponseAdd(data=Production_order_made_history_operations.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_operations_Update(request):
    return JsonResponse(DSResponseUpdate(data=Production_order_made_history_operations.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_operations_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history_operations.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_operations_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history_operations.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_operations_Info(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history_operations.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_operations_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history_operations.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
