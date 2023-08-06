from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.production_order_made_history_grouped_view import Production_order_made_history_grouped_view, Production_order_made_history_grouped_viewManager


@JsonResponseWithException()
def Production_order_made_history_grouped_view_Fetch(request):
    _request = DSRequest(request)
    if _request.user.is_admin or _request.user.is_develop:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order_made_history_grouped_view.objects.
                    select_related('exucutor').
                    get_range_rows1(
                    request=request,
                    function=Production_order_made_history_grouped_viewManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)
    else:
        return JsonResponse(
            DSResponse(
                request=request,
                data=Production_order_made_history_grouped_view.objects.
                    filter(exucutor=_request.user).
                    select_related('exucutor').
                    get_range_rows1(
                    request=request,
                    function=Production_order_made_history_grouped_viewManager.getRecord
                ),
                status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_grouped_view_Add(request):
    return JsonResponse(DSResponseAdd(data=Production_order_made_history_grouped_view.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_grouped_view_Update(request):
    return JsonResponse(DSResponseUpdate(data=Production_order_made_history_grouped_view.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_grouped_view_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history_grouped_view.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_grouped_view_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history_grouped_view.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_grouped_view_Info(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history_grouped_view.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Production_order_made_history_grouped_view_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Production_order_made_history_grouped_view.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
