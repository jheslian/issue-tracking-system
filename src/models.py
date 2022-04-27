from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Project(models.Model):
    type_choices = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('iOS', 'iOS'),
        ('android', 'Android')
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    type = models.CharField(max_length=20, choices=type_choices)


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission_choices = [
        ('contributor', 'Contributeur'),
        ('author', 'Autheur'),
    ]
    permission = models.CharField(choices=permission_choices, max_length=20)
    role = models.CharField(max_length=30)


class Issue(models.Model):
    tag_choices = [
        ('bug', 'Bug'),
        ('improvement', 'Amélioration'),
        ('task', 'Tâche')
    ]
    status_choices = [
        ('to-do', 'A faire'),
        ('on-proces', 'En cours'),
        ('done', 'Terminé')
    ]
    priority_choices = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Elvée')
    ]
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    tag = models.CharField(max_length=20, choices=tag_choices)
    priority = models.CharField(max_length=20, choices=priority_choices)
    status = models.CharField(max_length=20, choices=status_choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_issue')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)


class Comment(models.Model):
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)
