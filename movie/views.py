from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
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
from .models import Category, Character, Comment, Crew, CrewCharacter,CrewProfession,Language, Movie, MovieCategory, MovieCrew, MovieLanguage, MovieRegion, Password, Profession, Region, Role, User, UserRole
# Create your views here.
# Create your views here.



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        conn = pymysql.connect(host='134.209.169.96',
                           port=3306,
                           user='MovieSystem',
                           passwd='M0vie$ystem123',
                           db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        if cursor.execute("select * from user INNER JOIN password ON user.userId = password.userId where user.userId =%s and password.password=%s",
                        [
                            username,
                            password,
                        ]):
            if cursor.execute("select * from user INNER JOIN user_role ON user.userId = user_role.userId INNER JOIN role ON user_role.roleId = role.roleId where user.userId =%s and role.type=%s",
                        [
                            username,
                            role,
                        ]):
                if role == "admin":
                    return redirect('/movie_manage')
                else:
                    return redirect('/movie')
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
        cursor.close()
        conn.commit()
        conn.close()
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conn = pymysql.connect(host='134.209.169.96',
                           port=3306,
                           user='MovieSystem',
                           passwd='M0vie$ystem123',
                           db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into user values(%s,%s,%s,%s);",
                       (username, firstname, lastname, email))
        cursor.execute("insert into password values(%s,%s);",
                       (username, password))
        conn.commit()
        cursor.close()
        conn.close()
    return render(request, 'signup.html')
    # else:
    #     return render(request, 'login.html')



    #     a = User.objects.all()
    #     user = authenticate(username=username, password=password)
    #     if user and user.is_active:
    #         login(request, user)
    #         return redirect('/movie.html')
    # return HttpResponse("Hello, world. You're at the polls index.")



def movie(request):
    conn = pymysql.connect(host='134.209.169.96',
                           port=3306,
                           user='MovieSystem',
                           passwd='M0vie$ystem123',
                           db='movie_system')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from movie limit 0,200")
    movie_list = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return render(request, 'movie.html', {
        'movie_list': movie_list,
        'show': 1
    })

def movie_manage(request):
    conn = pymysql.connect(host='134.209.169.96',
                           port=3306,
                           user='MovieSystem',
                           passwd='M0vie$ystem123',
                           db='movie_system')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from movie limit 0,200")
    movie_list = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return render(request, 'movie_manage.html', {
        'movie_list': movie_list,
        'show': 1
    })

def search(request):
    if request.method == "POST":
        info = request.POST.get('info')
        print(info)
        conn = pymysql.connect(host='134.209.169.96',
                            port=3306,
                            user='MovieSystem',
                            passwd='M0vie$ystem123',
                            db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select * from movie where movie.primaryTitle like %s or movie.movie_id = %s or originalTitle = %s or releaseYear = %s limit 0,200",
                        [
                            info,
                            info,
                            info,
                            info,
                        ])
        movie_list = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return render(request, 'movie.html', {
            'movie_list': movie_list,
            'show': 1
        })


def edit_movie(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        conn = pymysql.connect( host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select * from movie where movie_id=%s", [
            nid,
        ])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request, 'edit_movie.html', {'result': result})
    else:
        nid = request.POST.get('id')
        primaryTitle = request.POST.get('primaryTitle')
        originalTitle = request.POST.get('originalTitle')
        conn = pymysql.connect(host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(
            "update movie set primaryTitle=%s,originalTitle=%s", 
            [
                primaryTitle,
                originalTitle,
            ])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/movie_manage.html')

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

def home(request):
    name_list = [] 
    data_list = []
    time_list=[]
    movie_list = Movie.objects.filter(movie_id__lt=1000000)
    for i in movie_list:
        name_list.append(i.movie_id)
        data_list.append(i.averagerating)
        time_list.append(i.releaseyear)
    print(name_list)
    return render(request, 'home.html',{'name':name_list,'data_list': data_list,'time':time_list})  


def base(request):
    pass

def logintext(request):
    
    return render(request, 'logintext.html')