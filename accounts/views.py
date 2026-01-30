# accounts/views.py
 
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView  # ListView をインポート
from django.contrib.auth.mixins import LoginRequiredMixin # ログイン必須機能
from .forms import SignUpForm
# from webshopapp.models import Order  # webshopappからOrderモデルをインポート
 
# --- 新規会員登録ビュー ---
class SignUpView(CreateView):
    # 使うフォームを指定
    form_class = SignUpForm
    # 登録成功後にリダイレクトするURLを指定
    success_url = reverse_lazy('accounts:login') 
    # 表示するテンプレートファイルを指定
    template_name = 'accounts/signup.html'
