"""djangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventory import views
from django.conf import settings
from django.conf.urls.static import static
from inventory import models
urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_quest',views.create_quest),
    path('get_inventory', views.get_inventory, name='get_inventory'),
    path('',views.read),
    # path('order_inventory/<int:id>',views.order_inventory),
    # path('create_order/<int:id>',views.create_order),
    # path('update/<int:id>',views.update),
    # path('delete/<int:id>',views.delete),
    # path('export_to_csv',views.export_to_csv),
    # path('empty',views.read),
    # path('calculate_shipment/<int:id>',views.calculate_shipment),

   
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
