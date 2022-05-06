from django.urls import path
from src.views import ProjectView, ProjectDetailView, ContributorView, ContributorDetailView, IssueView, \
    IssueDetailView, CommentsView, CommentDetailView

urlpatterns = [
    path('', ProjectView.as_view(), name='project'),
    path('<int:project_id>', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:project_id>/users/', ContributorView.as_view()),
    path('<int:project_id>/users/<int:user_id>', ContributorDetailView.as_view()),
    path('<int:project_id>/issues/', IssueView.as_view()),
    path('<int:project_id>/issues/<int:id>', IssueDetailView.as_view()),
    path('<int:project_id>/issues/<int:issue_id>/comments/', CommentsView.as_view()),
    path('<int:project_id>/issues/<int:issue_id>/comments/<int:id>', CommentDetailView.as_view()),
]
