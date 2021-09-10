from django.urls import path

from . import views

app_name = "languages"

urlpatterns = [
    path('', views.LanguageList.as_view(), name='language-list'),
    path('<int:pk>', views.LanguageDetail.as_view(), name='language-detail'),
]