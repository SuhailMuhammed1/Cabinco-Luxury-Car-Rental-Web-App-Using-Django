from django.urls import path
from cabapp import views

urlpatterns = [
    path('', views.index), 
    path('cars/', views.cars),
    path('contact_us/', views.contact_us),
    path('admin/', views.admin),
    # path('admin_reg/', views.admin_reg),
    path('admin_login/',views.admin_login),
    path('admin_logout/',views.admin_logout),
    path('admin_view_profile/',views.admin_view_profile),
    path('admin_update_profile/',views.admin_update_profile),
    path('admin_view_update_profile/',views.admin_view_update_profile),
    path('add_car/',views.add_car),
    path('view_car/',views.view_car),
    path('view_single_car/',views.view_single_car),
    path('delete_car/',views.delete_car),
    path('update_car/',views.update_car),
    path('view_update_car/',views.view_update_car),

]

handler404 = views.custom_404_view
