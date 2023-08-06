from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.ckk.models.item import Item, ItemManager


@JsonResponseWithException()
def Item_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item.objects.
                select_related(
                'STMP_1',
                'STMP_2',
                'document',
                'lotsman_document',
            ).
                get_range_rows1(
                request=request,
                function=ItemManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_Add(request):
    return JsonResponse(DSResponseAdd(data=Item.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_Update(request):
    return JsonResponse(DSResponseUpdate(data=Item.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)

@JsonResponseWithException()
def Item_Replace(request):
    return JsonResponse(DSResponseUpdate(data=Item.objects.replaceFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_Info(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_CheckRecursives(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.checkRecursives(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def GetQtyChilds(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.getQtyChilds(request=request), status=RPCResponseConstant.statusSuccess).response)

@JsonResponseWithException()
def GetGrouping(request):
    return JsonResponse(DSResponse(request=request, data=Item.objects.getGrouping(request=request), status=RPCResponseConstant.statusSuccess).response)
