from django.urls import path

from kaf_pas.planing.views import production_order_tmp

urlpatterns = [

    path('Production_order_tmp/Fetch/', production_order_tmp.Production_order_tmp_Fetch),
    path('Production_order_tmp/Add', production_order_tmp.Production_order_tmp_Add),
    path('Production_order_tmp/Update', production_order_tmp.Production_order_tmp_Update),
    path('Production_order_tmp/Remove', production_order_tmp.Production_order_tmp_Remove),
    path('Production_order_tmp/Lookup/', production_order_tmp.Production_order_tmp_Lookup),
    path('Production_order_tmp/Info/', production_order_tmp.Production_order_tmp_Info),
    path('Production_order_tmp/Count/', production_order_tmp.Production_order_tmp_Count),
    path('Production_order_tmp/Check/', production_order_tmp.Production_order_tmp_Check),
    path('Production_order_tmp/SetCount', production_order_tmp.Production_order_tmp_SetCount),
    path('Production_order_tmp/Copy', production_order_tmp.Production_order_tmp_Copy),

]
