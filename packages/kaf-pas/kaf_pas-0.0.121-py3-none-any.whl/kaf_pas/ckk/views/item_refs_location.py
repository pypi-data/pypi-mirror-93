from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.ckk.models.item_refs_location import Item_refs_location
from kaf_pas.ckk.models.item_refs_location_view import Item_refs_location_view, Item_refs_location_viewManager


@JsonResponseWithException()
def Item_refs_location_Fetch(request):
    _request = DSRequest(request)
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_refs_location_view.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Item_refs_location_viewManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_refs_location_Add(request):
    return JsonResponse(DSResponseAdd(data=Item_refs_location.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_refs_location_Update(request):
    return JsonResponse(DSResponseUpdate(data=Item_refs_location.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_refs_location_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Item_refs_location.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_refs_location_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Item_refs_location.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_refs_location_Info(request):
    return JsonResponse(DSResponse(request=request, data=Item_refs_location.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_refs_location_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Item_refs_location.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
