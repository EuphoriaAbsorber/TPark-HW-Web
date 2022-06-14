"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from app import views
from django.contrib.auth.views import LogoutView

from askme.settings import LOGOUT_REDIRECT_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('ask', views.ask, name="ask"),
    path('question/<int:id>', views.question, name="question"),
    path('login', views.Login, name="login"),
    path('signup', views.signup, name="signup"),
    path('hot', views.hot, name="hot"),
    path('tag/<str:s>', views.tag, name="tag"),
    path('logout/', LogoutView.as_view(next_page = LOGOUT_REDIRECT_URL), name = "logout"),
    path('settings', views.settings, name="settings"),
    re_path(r'^', views.handler404),
]
