from django.contrib import admin
from .models import User, Contributor, Comment, Project, Issue


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'last_name')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user_id','user', 'project')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','issue', 'description', 'author')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'title', 'tag', 'priority')


admin.site.register(User, UserAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
