from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager


# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.last_name


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

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission_choices = [
        ('contributor', 'Contributeur'),
        ('author', 'Autheur'),
    ]
    permission = models.CharField(choices=permission_choices, max_length=20)
    role = models.CharField(max_length=30)

    def __str__(self):
        return self.user.last_name


class Issue(models.Model):
    tag_choices = [
        ('bug', 'Bug'),
        ('improvement', 'Amélioration'),
        ('task', 'Tâche')
    ]
    status_choices = [
        ('to_do', 'A faire'),
        ('on_proces', 'En cours'),
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_issue', null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment',  null=True, blank=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE,  null=True, blank=True)
    created_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.description
