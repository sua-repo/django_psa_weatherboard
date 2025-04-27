# dev_16 : 회원가입 폼
from django import forms
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="아이디")
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
    real_name = forms.CharField(max_length=100, label="이름")
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="생년월일"
    )
    gender = forms.ChoiceField(choices=[("F", "여자"), ("M", "남자")], label="성별")

    cold_sensitivity = forms.ChoiceField(
        choices=[("민감", "민감"), ("보통", "보통"), ("둔감", "둔감")],
        label="추위 민감도",
    )
    heat_sensitivity = forms.ChoiceField(
        choices=[("민감", "민감"), ("보통", "보통"), ("둔감", "둔감")],
        label="더위 민감도",
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # 비밀번호 암호화

        if commit:
            user.save()

            # 프로필 생성
            Profile.objects.create(
                user=user,
                real_name=self.cleaned_data["real_name"],
                birthdate=self.cleaned_data["birthdate"],
                gender=self.cleaned_data["gender"],
                cold_sensitivity=self.cleaned_data["cold_sensitivity"],
                heat_sensitivity=self.cleaned_data["heat_sensitivity"],
            )
        return user
