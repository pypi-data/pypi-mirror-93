from django.urls import path

from kaf_pas.kd.views import uploades

urlpatterns = [

    path('Uploades/Fetch/', uploades.Uploades_Fetch),
    path('Uploades/Add', uploades.Uploades_Add),
    path('Uploades/Calc', uploades.Uploades_Calc),
    path('Uploades/Update', uploades.Uploades_Update),
    path('Uploades/Remove', uploades.Uploades_Remove),
    path('Uploades/Lookup/', uploades.Uploades_Lookup),
    path('Uploades/Info/', uploades.Uploades_Info),
    path('Uploades/Copy', uploades.Uploades_Copy),
    path('Uploades/Confirmation', uploades.Uploades_Confirmation),
    path('Uploades/UnConfirmation', uploades.Uploades_UnConfirmation),

]
