from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector
import datetime
import pymysql
import time
import pytz
import logging
import json
# Put the logging info within your django view
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
# from django.contrib.auth.models import User
from .models import Category, Character, Comment, Crew, CrewCharacter,CrewProfession,Language, Movie, MovieCategory, MovieCrew, MovieLanguage, MovieRegion, Password, Profession, Region, Role, User, UserRole, Recommend
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
        cursor.execute("insert into user_role values('1',%s);",
                       username)
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
    nid = request.GET.get('nid')
    if nid:
        conn = pymysql.connect( host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select movie_id,primaryTitle,originalTitle,averageRating from movie where movie_id =%s;",[
            nid,
        ])
        a = cursor.fetchone()
        print(a)

        # movie_list = Movie.objects.get(movie_id=int(nid))
        try:
            cursor.execute("insert into recommend values(%s,%s,%s,%s,0);" ,(
                a['movie_id'],
                a['primaryTitle'],
                a['originalTitle'],
                a['averageRating'],
            ))
            conn.commit()
        except:
            pass
        cursor.close()
        conn.close()
    return render(request, 'movie.html', {
        'movie_list': movie_list,
        'show': 1
    })

def movie_detail(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect( host='134.209.169.96',
                            port=3306,
                            user='MovieSystem',
                            passwd='M0vie$ystem123',
                            db='movie_system')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select movie.movie_id, movie.movie_id, movie.primaryTitle, movie.originalTitle, movie.runtimeMinutes, movie.isAdult, movie.releaseYear, movie.averageRating, category.name,language.name as language, region.name as region, crew.primaryName as crew from movie join movie_category on movie.movie_id=movie_category.movie_id join category on movie_category.category_id=category.category_id join movie_language on movie.movie_id=movie_language.movie_id join language on movie_language.languageId=language.languageId join movie_region on movie.movie_id=movie_region.movie_id join region on movie_region.region_id=region.region_id join movie_crew on movie.movie_id=movie_crew.movieId join crew on movie_crew.crewId=crew.crewId where movie.movie_id=%s", [
        nid,
    ])
    result = cursor.fetchone()
    print(result)
    cursor.close()
    conn.close()
    return render(request, 'movie_detail.html', {'result': result})

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
        cursor.execute("select * from movie where movie.primaryTitle like %s or movie.movie_id = %s or originalTitle = %s or releaseYear = %s or averageRating = %s or runtimeMinutes = %s limit 0,200",
                        [
                            info,
                            info,
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

def search_movie(request):
    if request.method == "POST":
        info = request.POST.get('info')
        print(info)
        conn = pymysql.connect(host='134.209.169.96',
                            port=3306,
                            user='MovieSystem',
                            passwd='M0vie$ystem123',
                            db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select * from movie where movie.primaryTitle like %s or movie.movie_id = %s or originalTitle = %s or releaseYear = %s or averageRating = %s or runtimeMinutes = %s limit 0,200",
                        [
                            info,
                            info,
                            info,
                            info,
                            info,
                            info,
                        ])
        movie_list = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return render(request, 'movie_manage.html', {
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
        print(result)
        cursor.close()
        conn.close()
        return render(request, 'edit_movie.html', {'result': result})
    else:
        nid = request.POST.get('nid')
        primaryTitle = request.POST.get('primaryTitle')
        originalTitle = request.POST.get('originalTitle')
        print(nid)
        print(originalTitle)
        conn = pymysql.connect(host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(
            "update movie set primaryTitle=%s,originalTitle=%s where movie_id=%s", 
            [
                primaryTitle,
                originalTitle,
                nid,
            ])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/movie_manage')

def del_movie(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from movie where movie_id=%s", [
        nid,
    ])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/movie_manage/')

def recommend(request):
        conn = pymysql.connect( host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select * from recommend")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(request, 'recommend.html', {'result': result})

def del_recommend(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from recommend where movie_id=%s", [
        nid,
    ])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/recommend/')

def myrating(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        conn = pymysql.connect( host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select * from recommend where movie_id=%s", [
            nid,
        ])
        result = cursor.fetchone()
        print(result)
        cursor.close()
        conn.close()
        return render(request, 'myrating.html', {'result': result})
    else:
        nid = request.POST.get('nid')
        primaryTitle = request.POST.get('primaryTitle')
        originalTitle = request.POST.get('originalTitle')
        averageRating = request.POST.get('averageRating')
        myRating = request.POST.get('myRating')
        print(nid)
        print(originalTitle)
        conn = pymysql.connect(host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(
            "update recommend set myRating=%s where movie_id=%s", 
            [
                myRating,
                nid,
            ])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/recommend')

def user_manage(request):
    conn = pymysql.connect(host='134.209.169.96',
                           port=3306,
                           user='MovieSystem',
                           passwd='M0vie$ystem123',
                           db='movie_system')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select user.userId, user.firstName, user.lastName, user.emailAddress, password.password, role.type from user join password on user.userId=password.userId join user_role on user.userId=user_role.userId join role on user_role.roleId=role.roleId")
    user_list = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return render(request, 'user_manage.html', {
        'user_list': user_list,
        'show': 1
    })

def search_user(request):
    if request.method == "POST":
        info = request.POST.get('info')
        print(info)
        conn = pymysql.connect(host='134.209.169.96',
                            port=3306,
                            user='MovieSystem',
                            passwd='M0vie$ystem123',
                            db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select user.userId, user.firstName, user.lastName, user.emailAddress, password.password, role.type from user join password on user.userId=password.userId join user_role on user.userId=user_role.userId join role on user_role.roleId=role.roleId where user.userId = %s or user.firstName = %s or user.lastName = %s or user.emailAddress = %s limit 0,200",
                        [
                            info,
                            info,
                            info,
                            info,
                        ])
        user_list = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return render(request, 'user_manage.html', {
            'user_list': user_list,
            'show': 1
        })


def del_user(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from user where userId=%s", [
        nid,
    ])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/user_manage/')

def edit_user(request):
    if request.method == "GET":
        userId = request.GET.get('userId')
        conn = pymysql.connect( host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select user.userId, user.firstName, user.lastName, user.emailAddress, password.password, role.type from user join password on user.userId=password.userId join user_role on user.userId=user_role.userId join role on user_role.roleId=role.roleId where user.userId=%s", [
            userId,
        ])
        result = cursor.fetchone()
        print(result)
        cursor.close()
        conn.close()
        return render(request, 'edit_user.html', {'result': result})
    else:
        userId = request.POST.get('userId')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        emailAddress = request.POST.get('emailAddress')
        password = request.POST.get('password')
        roletype = request.POST.get('type')
        if roletype == 'user':
            role = 1
        else:
            role = 2
        print(roletype)
        print(emailAddress)
        conn = pymysql.connect(host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(
            "update user join password on user.userId=password.userId join user_role on user.userId=user_role.userId join role on user_role.roleId=role.roleId set user.firstName=%s,user.lastName=%s,user.emailAddress=%s,password.password=%s,user_role.roleId=%s where user.userId=%s", 
            [
                firstName,
                lastName,
                emailAddress,
                password,
                role,
                userId,
            ])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/user_manage')

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

def index(request):
    return render(request, 'index.html')

def home(request):
    name_list = [] 
    data_list = []
    time_list=[]
    movie_list = Movie.objects.filter(movie_id__range=[100000,200000]).order_by("releaseyear")
    for i in movie_list:
        name_list.append(i.movie_id)
        data_list.append(i.averagerating)
        time_list.append(i.releaseyear)
    print(name_list)
    print(time_list)
    return JsonResponse({'name':name_list,'data_list': data_list,'time':time_list})  


def base(request):
    # utils = rpackages.importr('utils')
    # packnames = ('tidyverse', 'tidyr', 'cluster', 'dplyr', 'readxl', 'caret')
    # names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
    # print(names_to_install)
    # if len(names_to_install) > 0:
    #     utils.install_packages(StrVector(names_to_install))
    # # try:
    # robjects.r.source("algorithm/movie_recommend.R")
    # print(robjects.r("res2"))
    # except Exception as e:
    #     print(e)
    # utils = rpackages.importr('utils')
    # packages = ('tidyverse', 'tidyr', 'cluster', 'dplyr', 'readxl', 'caret', 'readxl')
    # names_to_install = [x for x in packages if not rpackages.isinstalled(x)]
    # print("packages: ",names_to_install)
    # if len(packages) > 0:
    #     utils.install_packages(StrVector(names_to_install))
    # try:
    #     robjects.r.source("movie_recommend.R")
    #     res = robjects.r("res2")
    #     for i in list(res[0]):
    #         print("movieId: ", i)
    res_list = [1000361, 1001110, 1002299, 1002308, 1002317]
    print(res_list[0])
    conn = pymysql.connect( host='134.209.169.96',
                                port=3306,
                                user='MovieSystem',
                                passwd='M0vie$ystem123',
                                db='movie_system')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from movie where movie_id=%s or movie_id=%s or movie_id=%s or movie_id=%s or movie_id=%s ", [
        res_list[0],
        res_list[1],
        res_list[2],
        res_list[3],
        res_list[4],
    ])
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'base.html', {'result': result})

def logintext(request):
    
    return render(request, 'logintext.html')