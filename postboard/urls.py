"""post_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from postboard import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.main),
    path('daily/', views.daily, name='daily'),
    path('insert/', views.insert, name='insert'),
    # path('daily/<int:id>', views.daily2),
    path('viewwork/<int:id>', views.viewwork, name='viewwork'),
    path('writeBoard/', views.writeBoard),
    path('updateBoard/<int:id>', views.updateBoard),
    path('delBoard/', views.delBoard, name='delBoard'),
    # path('upload1/', views.upload1, name='upload1'),
    # path('upload2/', views.upload2, name='upload2'),

]
