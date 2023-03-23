from django.urls import path
from .views import *
urlpatterns = [
    path("register",RegiserView.as_view()),
    path('fetchusers',FetchUsers.as_view()),
    path('documentdata/<int:id>',FetchDocumentData.as_view()),
    path('name_match/<str:givenname>/<str:id_name>',NameMatchPercentage.as_view())
]
