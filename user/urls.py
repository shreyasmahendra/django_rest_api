from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('api/', views.SnippetList.as_view()),
    path('api/auth/', views.AuthList.as_view()),
    path('api/<int:pk>/', views.SnippetDetail.as_view()),
    path('api/patch/<int:pk>',views.patch_api),
]

urlpatterns = format_suffix_patterns(urlpatterns)

