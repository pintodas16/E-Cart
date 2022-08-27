
from django.urls import path
from . import views




urlpatterns = [
    path('place_order/',views.place_order, name = 'place_order'),
    path('payments/',views.payments, name = 'payments'),
    path('status/',views.sslc_status,name='status'),
    path('sslc/complete/<val_id>/<tran_id>/',views.sslc_complete,name = 'sslc_complete'),
    path('order_complete/',views.order_complete, name = 'order_complete'),
    
] 
