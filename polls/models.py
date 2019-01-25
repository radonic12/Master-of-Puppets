from django.db import models

# Create your models here.

class Users(models.Model):
    usrnme = models.TextField()
    psswrd = models.TextField()
    unqKey = models.TextField(default="",blank=True)

    def _str_(self):
        return

class Project(models.Model):
    unqKey = models.TextField()
    nme = models.TextField(blank=True)
    cde = models.TextField(blank=True)
    actve = models.TextField(blank=True)

    def _str_(self):
        return

class LstUsd(models.Model):
    dte = models.DateTimeField(auto_now_add=True)
    unqKey = models.TextField(default="",blank=True)

    def _str_(self):
        return