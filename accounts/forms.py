# accounts/forms.py
 
from django import forms
from django.db import transaction
from .models import CustomUser
 
# UserCreationFormに頼らず、ModelFormから直接作成
class SignUpForm(forms.ModelForm):
    # --- 1. 表示する全ての入力欄を、ここで明示的に定義 ---
 
    # パスワード入力欄（1つ目：本体）
    password = forms.CharField(
        label="パスワード",
        strip=False,  # 入力値の前後から空白を削除しない
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
 
    # パスワード入力欄（2つ目：確認用）
    password2 = forms.CharField(
        label="パスワード（確認用）",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
 
    # --- 2. どのモデルを元にするか、どのモデルの項目を使うかを定義 ---
    class Meta:
        model = CustomUser
        fields = ('email', 'birthday')
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }
 
 
    # passwordとpassword2が一致するかをチェックする
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        return password2
 
    # ユーザーをデータベースに保存する処理
    @transaction.atomic
    def save(self, commit=True):
        # Metaで定義したemailとbirthdayを持つユーザーオブジェクトを作成
        user = super().save(commit=False)
        # usernameにemailをセット
        user.username = self.cleaned_data['email']
        # パスワードを安全な形式（ハッシュ化）にしてセット
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user