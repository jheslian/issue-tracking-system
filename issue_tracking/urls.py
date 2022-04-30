"""issue_tracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from src.views import ProjectView, ProjectDetailView, ContributorView, ContributorDetailView, IssueView, \
    IssueDetailView, CommentsView, CommentDetailView, RegisterUser


router = SimpleRouter()
router.register('signup', RegisterUser, basename='signup'),


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('signup/', RegisterUser.as_view()),
    #path('logout/', logout),
    path('project/', ProjectView.as_view(), name='project'),
    path('project/<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/users/', ContributorView.as_view(), ),
    path('project/<int:project_id>/users/<int:user_id>', ContributorDetailView.as_view(), ),
    path('project/<int:pk>/issues/', IssueView.as_view(), ),
    path('project/<int:project_id>/issues/<int:id>', IssueDetailView.as_view(), ),
    path('project/<int:project_id>/issues/<int:issue_id>/comments/', CommentsView.as_view(), ),
    path('project/<int:project_id>/issues/<int:issue_id>/comments/<int:id>', CommentDetailView.as_view(), ),

    path('', include(router.urls)),
]

