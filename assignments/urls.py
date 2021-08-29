from django.urls import path, include
from . import views

urlpatterns = [
    path("assignment/create", views.CreateAssignment.as_view(), name="assignment-create"),
    path("assignment/<int:id>", views.UpdateDeleteAssignment.as_view(), name="assignment-update"),
    path("assignment/<int:assignment_id>/submit", views.SubmitAssignment.as_view(),
         name="submission-update"),
    path("assignment/<int:assignment_id>/details", views.AssignmentDetails.as_view(), name="assignment-details"),
    path("assignment/feed", views.AssigmentFeed.as_view(), name="assignment-feed"),
]
