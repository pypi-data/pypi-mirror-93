from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.accounting.models.tmp_buffer import Tmp_buffer, Tmp_bufferManager


@JsonResponseWithException()
def Tmp_buffer_Fetch(request):
    _request = DSRequest(request=request)

    return JsonResponse(
        DSResponse(
            request=request,
            data=Tmp_buffer.objects.
                filter(user_id=_request.user_id, props=1).
                get_range_rows1(
                request=request,
                function=Tmp_bufferManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Tmp_buffer_Fetch1(request):
    from kaf_pas.accounting.models.buffers import Buffers

    req = DSRequest(request=request)
    Tmp_buffer.objects.filter(user=req.user, props__in=[2, 4]).delete()
    for buffers in Buffers.objects.filter(value__lt=0):
        Tmp_buffer.objects.create(
            color=buffers.color,
            demand=buffers.demand,
            edizm=buffers.edizm,
            item=buffers.item,
            location=buffers.location,
            launch=buffers.launch,
            props=2,
            user=req.user,
            value=buffers.value,
        )

    return JsonResponse(
        DSResponse(
            request=request,
            data=Tmp_buffer.objects.
                filter(user=req.user).
                get_range_rows1(
                request=request,
                function=Tmp_bufferManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Tmp_buffer_hover_Fetch1(request):
    req = DSRequest(request=request)

    return JsonResponse(
        DSResponse(
            request=request,
            data=Tmp_buffer.objects.
                filter(user=req.user, props=2).
                get_range_rows1(
                request=request,
                function=Tmp_bufferManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Tmp_buffer_Add(request):
    return JsonResponse(DSResponseAdd(data=Tmp_buffer.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Tmp_buffer_Update(request):
    return JsonResponse(DSResponseUpdate(data=Tmp_buffer.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Tmp_buffer_Update1(request):
    return JsonResponse(DSResponseUpdate(data=Tmp_buffer.objects.update_offFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Tmp_buffer_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Tmp_buffer.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Tmp_buffer_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Tmp_buffer.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Tmp_buffer_Info(request):
    return JsonResponse(DSResponse(request=request, data=Tmp_buffer.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Tmp_buffer_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Tmp_buffer.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
