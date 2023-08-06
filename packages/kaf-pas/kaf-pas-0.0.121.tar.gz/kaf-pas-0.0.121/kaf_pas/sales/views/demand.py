from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException, JsonWSResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.sales.models.demand import Demand
from kaf_pas.sales.models.demand_view import Demand_view, Demand_viewManager


@JsonResponseWithException()
def Demand_Fetch(request):
    _request = DSRequest(request)
    return JsonResponse(
        DSResponse(
            request=request,
            data=Demand_view.objects.
                get_range_rows1(
                request=request,
                function=Demand_viewManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Demand_Fetch4(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Demand_view.objects.
                get_range_rows1(
                request=request,
                function=Demand_viewManager.getRecord1
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Demand_Add(request):
    return JsonResponse(DSResponseAdd(data=Demand.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonWSResponseWithException()
def Demand_Update(request):
    return JsonResponse(DSResponseUpdate(data=Demand.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Demand_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Demand.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Demand_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Demand.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Demand_Info(request):
    return JsonResponse(DSResponse(request=request, data=Demand_view.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Demand_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Demand.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
