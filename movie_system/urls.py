"""movie_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include, re_path
from movie import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('movie/', include('movie.urls')),
    path('login/', views.login),
    path('signup/', views.signup),
    path('base/', views.base),
    path('movie/', views.movie),
    path('add_user/', views.add_user),
    path('user_manage/', views.user_manage),
    path('search_user/', views.search_user),
    path('del_user/', views.del_user),
    path('edit_user/', views.edit_user),
    path('search/', views.search),
    path('search_movie/', views.search_movie),
    path('movie_manage/', views.movie_manage),
    path('edit_movie/', views.edit_movie),
    path('home/', views.home),
    path('echarts/', views.index),
    path('recommend/', views.recommend),
    path('del_movie/', views.del_movie),
    path('movie_detail/', views.movie_detail),
    path('myrating/', views.myrating),
    path('index/', views.index),
    path('liked', views.movie_like),
    path('unliked', views.movie_unlike),
    re_path(r'^$',views.movie)
]
