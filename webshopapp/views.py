from django.shortcuts import render
from django.views.generic import TemplateView

class TopView(TemplateView):
    template_name = "webshopapp/top.html"

class TemplateListView(TemplateView):
    template_name = "webshopapp/template-list.html"

class TemplateDetailView(TemplateView):
    template_name = "webshopapp/template-detail.html"

class SignUpView(TemplateView):
    template_name = "webshopapp/signup.html"

class ResetPasswordView(TemplateView):
    template_name = "webshopapp/reset-password.html"

class RegisterView(TemplateView):
    template_name = "webshopapp/register.html"

class LoginView(TemplateView):
    template_name = "webshopapp/login.html"

class ForgotPasswordView(TemplateView):
    template_name = "webshopapp/forgot-password.html"