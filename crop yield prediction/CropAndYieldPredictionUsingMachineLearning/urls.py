from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from cropandyield.views import predict,predictAction

urlpatterns = [

    path('admin/', admin.site.urls),

    path('',TemplateView.as_view(template_name = 'index.html'),name='index'),
    path('index/',TemplateView.as_view(template_name = 'index.html'),name='index'),

    path('predict/',predict,name='predict'),
    path('predictaction/',predictAction,name='predictaction'),

]
