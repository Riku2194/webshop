"""
URL configuration for webshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from webshopapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TopView.as_view(), name="top"),
    path('template-list/', views.TemplateListView.as_view(), name="template-list"),
    path('template-detail/', views.TemplateDetailView.as_view(), name="template-detail"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('reset-password/', views.ResetPasswordView.as_view(), name="reset-password"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name="forgot-password"),
    path('payments/', include('payments.urls')),
]
