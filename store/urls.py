
from django.urls import path
from . import views




urlpatterns = [
    path('',views.store , name ='store'),
    path('category/<slug:category_slug>/',views.store, name = 'product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail, name = 'product_detail'),
    path('search/',views.search,name = 'search'),
    path('submit_review/<int:product_id>',views.submit_review, name='submit_review'),
    
    path('category/',views.laptop_latest_product, name = 'laptop_latest_product'),
    path('category/television/',views.television_latest_product, name = 'television_latest_product'),
    path('category/mobile-phone',views.mobile_phone_latest_product, name = 'mobile-phone_latest_product'),
    path('category/head-phone/',views.head_phone_latest_product, name = 'head-phone_latest_product'),
    
    # path('<slug:category_slug>/<slug:product_slug>/',views.product_detatil , name = 'product_detail'),
] 
