from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.production_order_values import Production_order_valuesManager, Production_order_values


@JsonResponseWithException()
def Production_order_values_Fetch(request):
    _request = DSRequest(request=request)
    if _request.user.is_admin or _request.user.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order_values.objects.
                    filter().
                    get_range_rows1(
                    request=request,
                    function=Production_order_valuesManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        from kaf_pas.planing.models.operation_types import Operation_types
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order_values.objects.
                    exclude(opertype__props=Operation_types.props.minus).
                    get_range_rows1(
                    request=request,
                    function=Production_order_valuesManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_values_Add(request):
    return JsonResponse(DSResponseAdd(data=Production_order_values.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_values_AddBlock(request):
    return JsonResponse(DSResponseAdd(data=Production_order_values.objects.createBlockFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_values_Update(request):
    return JsonResponse(DSResponseUpdate(data=Production_order_values.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_values_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_values.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_values_Lookup(request):
    # _request = DSRequest(request=request)
    return JsonResponse(DSResponse(request=request, data=Production_order_values.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_values_Info(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_values.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_values_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_values.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
