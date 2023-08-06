from django.urls import path

from kaf_pas.accounting.views import tmp_buffer

urlpatterns = [

    path('TmpBuffers/Fetch/', tmp_buffer.Tmp_buffer_Fetch),
    path('TmpBuffers/Fetch1/', tmp_buffer.Tmp_buffer_Fetch1),
    path('TmpBuffers_off_hover/Fetch1/', tmp_buffer.Tmp_buffer_hover_Fetch1),
    path('TmpBuffers/Add', tmp_buffer.Tmp_buffer_Add),
    path('TmpBuffers/Update', tmp_buffer.Tmp_buffer_Update),
    path('TmpBuffers/Update1', tmp_buffer.Tmp_buffer_Update1),
    path('TmpBuffers/Remove', tmp_buffer.Tmp_buffer_Remove),
    path('TmpBuffers/Lookup/', tmp_buffer.Tmp_buffer_Lookup),
    path('TmpBuffers/Info/', tmp_buffer.Tmp_buffer_Info),
    path('TmpBuffers/Copy', tmp_buffer.Tmp_buffer_Copy),

]
