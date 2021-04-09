# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = 'category'


class Character(models.Model):
    characterid = models.IntegerField(db_column='characterId', primary_key=True)  # Field name made lowercase.
    charactername = models.CharField(db_column='characterName', max_length=50)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'character'


class Comment(models.Model):
    movie = models.OneToOneField('Movie', models.DO_NOTHING, primary_key=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'comment'


class Crew(models.Model):
    crewid = models.CharField(db_column='crewId', primary_key=True, max_length=50)  # Field name made lowercase.
    primaryname = models.CharField(db_column='primaryName', max_length=50)  # Field name made lowercase.
    birthyear = models.IntegerField(db_column='birthYear', blank=True, null=True)  # Field name made lowercase.
    deathyear = models.IntegerField(db_column='deathYear', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'crew'


class CrewCharacter(models.Model):
    crewid = models.OneToOneField(Crew, models.DO_NOTHING, db_column='crewId', primary_key=True)  # Field name made lowercase.
    characterid = models.ForeignKey(Character, models.DO_NOTHING, db_column='characterId')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'crew_character'
        unique_together = (('crewid', 'characterid'),)


class CrewProfession(models.Model):
    crewid = models.OneToOneField(Crew, models.DO_NOTHING, db_column='crewId', primary_key=True)  # Field name made lowercase.
    professionid = models.ForeignKey('Profession', models.DO_NOTHING, db_column='professionId')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'crew_profession'
        unique_together = (('crewid', 'professionid'),)


class Language(models.Model):
    languageid = models.AutoField(db_column='languageId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = 'language'


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    primarytitle = models.CharField(db_column='primaryTitle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    originaltitle = models.CharField(db_column='originalTitle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    runtimeminutes = models.IntegerField(db_column='runtimeMinutes', blank=True, null=True)  # Field name made lowercase.
    isadult = models.IntegerField(db_column='isAdult', blank=True, null=True)  # Field name made lowercase.
    releaseyear = models.IntegerField(db_column='releaseYear', blank=True, null=True)  # Field name made lowercase.
    averagerating = models.IntegerField(db_column='averageRating', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'movie'


class MovieCategory(models.Model):
    movie = models.OneToOneField(Movie, models.DO_NOTHING, primary_key=True)
    category = models.ForeignKey(Category, models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'movie_category'
        unique_together = (('movie', 'category'),)


class MovieCrew(models.Model):
    movieid = models.OneToOneField(Movie, models.DO_NOTHING, db_column='movieId', primary_key=True)  # Field name made lowercase.
    crewid = models.ForeignKey(Crew, models.DO_NOTHING, db_column='crewId')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'movie_crew'
        unique_together = (('movieid', 'crewid'),)


class MovieLanguage(models.Model):
    movie = models.OneToOneField(Movie, models.DO_NOTHING, primary_key=True)
    languageid = models.ForeignKey(Language, models.DO_NOTHING, db_column='languageId')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'movie_language'
        unique_together = (('movie', 'languageid'),)


class MovieRegion(models.Model):
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    region = models.ForeignKey('Region', models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'movie_region'


class Password(models.Model):
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId', primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'password'


class Profession(models.Model):
    professionid = models.IntegerField(db_column='professionId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = 'profession'


class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = 'region'


class Role(models.Model):
    roleid = models.IntegerField(db_column='roleId', primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'role'


class User(models.Model):
    userid = models.IntegerField(db_column='userId', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='emailAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    upassword = models.CharField(max_length=50)
    class Meta:
        # managed = False
        db_table = 'user'


class UserRole(models.Model):
    roleid = models.OneToOneField(Role, models.DO_NOTHING, db_column='roleId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'user_role'
        unique_together = (('roleid', 'userid'),)
