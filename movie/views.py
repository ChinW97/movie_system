from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import datetime
import pymysql
import time
import pytz
import logging
# Put the logging info within your django view
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
# from django.contrib.auth.models import User
# from .models import Category, Character, Comment, Crew, CrewCharacter,CrewProfession,Language,Movie, MovieCategory, MovieCrew, MovieLanguage, MovieRegion, Password, Profession, Region, Role, User, UserRole



def tmp(request):
    return render(request, 'tmp.html')

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):

    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        messages.info(request, username)



        return redirect('/tmp/')
    else:
        return render(request, 'login.html')



def movie(request):
    conn = pymysql.connect(host='134.209.169.96',
                           port=3306,
                           user='MovieSystem',
                           passwd='M0vie$ystem123',
                           db='movie_system')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select distinct movie.movie_id, movie.primaryTitle, movie.originalTitle, movie.runtimeMinutes, movie.isAdult, movie.releaseYear, movie.averageRating from movie INNER JOIN movie_region ON movie.movie_id = movie_region.movie_id INNER JOIN region ON region.region_id = movie_region.region_id limit 0,200")
    movie_list = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return render(request, 'movie.html', {
        'movie_list': movie_list,
        'show': 1
    })

def add_user(request):
    if request.method == "GET":
        return render(request, 'add_user.html')
    else:
        print(request.POST)
        o = request.POST.get('userId')
        i = request.POST.get('firstName')
        p = request.POST.get('lastName')
        l = request.POST.get('email')
        conn = pymysql.connect( host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into user values(%s,%s,%s,%s);",
                       (o, i, p, l))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/movie.html')

def base(request):
    return render(request, 'base.html')

def logintext(request):
    
    return render(request, 'logintext.html')