# accounts/views.py
 
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView  # ListView をインポート
from django.contrib.auth.mixins import LoginRequiredMixin # ログイン必須機能
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
# from webshopapp.models import Order  # webshopappからOrderモデルをインポート
 
# --- 新規会員登録ビュー ---
class SignUpView(CreateView):
    # 使うフォームを指定
    form_class = SignUpForm
    # 登録成功後にリダイレクトするURLを指定
    success_url = reverse_lazy('accounts:login') 
    # 表示するテンプレートファイルを指定
    template_name = 'accounts/signup.html'

class CustomLoginView(LoginView):
    """
    ログイン後のリダイレクト先をユーザーの種類によって変更するカスタムログインビュー
    """
    def get_success_url(self):
        # ログインしたユーザーオブジェクトを取得
        user = self.request.user
 
        # もし、そのユーザーがスーパーユーザーなら
        if user.is_superuser:
            # 管理画面のURLを返す
            return '/admin/'
        # そうでなければ（一般ユーザーなら）
        else:
            # デフォルトの動作（settings.pyのLOGIN_REDIRECT_URL）に従う
            return super().get_success_url()
 