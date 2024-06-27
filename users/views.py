import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from utils import NotAuthenticatedUserMixin
from . import tasks
from .forms import UserRegisterForm, UserVerifyCodeForm, UserLoginForm, UserProfileEditForm
from .models import User, OtpCode


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'

    def get(self, request):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        return render(request, self.template_name, {'user': user})


class UserRegisterView(NotAuthenticatedUserMixin, View):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(1000, 9999)
            tasks.send_code_task.delay(cd['phone'], random_code)
            OtpCode.objects.create(phone_number=cd['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'full_name': cd['full_name'],
                'phone_number': cd['phone'],
                'email': cd['email'],
                'password': cd['password2'],
            }
            messages.success(request, 'we sent you a code', extra_tags='success')
            return redirect('users:user_register_verify')
        messages.warning(request, 'please enter valid values')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyView(NotAuthenticatedUserMixin, View):
    form_class = UserVerifyCodeForm
    template_name = 'users/verify.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'], user_session['full_name'],
                                         user_session['password'])
                code_instance.delete()
                messages.success(request, 'Wellcome!', extra_tags='success')
                return redirect('home:home')
            messages.error(request, 'this code is wrong', extra_tags='danger')
            return redirect('users:user_register_verify')
        return render(request, self.template_name, {'form': form})


class UserLoginView(NotAuthenticatedUserMixin, View):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                random_code = random.randint(1000, 9999)
                tasks.send_code_task.delay(cd['phone'], random_code)
                OtpCode.objects.create(phone_number=cd['phone'], code=random_code)
                request.session['user_login_info'] = {
                    'phone_number': cd['phone'],
                    'password': cd['password'],
                    'next': self.next,
                }
                messages.success(request, 'we sent you a code', extra_tags='success')
                return redirect('users:user_login_verify')
            messages.error(request, 'phone or password is invalid', extra_tags='warning')
        return render(request, self.template_name, {'form': form})


class UserLoginVerifyView(NotAuthenticatedUserMixin, View):
    form_class = UserVerifyCodeForm
    template_name = 'users/verify.html'

    def get(self, request):
        form = UserVerifyCodeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session['user_login_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = UserVerifyCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                user = authenticate(request, phone_number=user_session['phone_number'],
                                    password=user_session['password'])
                if user is not None:
                    login(request, user)
                    code_instance.delete()
                    messages.success(request, 'logged in successfully', extra_tags='success')
                    if user_session['next']:
                        return redirect(user_session['next'])
                    return redirect('home:home')
                messages.warning(request, 'phone or password is invalid', extra_tags='warning')
                return redirect('users:user_login_verify')
            messages.warning(request, 'code is invalid', extra_tags='warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logged out successfully', extra_tags='success')
        return redirect('home:home')


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'users/passwordreset/password_reset_form.html'
    success_url = reverse_lazy('users:user_password_reset_done')
    email_template_name = 'users/passwordreset/password_reset_email.html'


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'users/passwordreset/password_reset_done.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'users/passwordreset/password_reset_confirm.html'
    success_url = reverse_lazy('users:user_password_reset_complete')


class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'users/passwordreset/password_reset_complete.html'


class UserProfileEditView(LoginRequiredMixin, View):
    form_class = UserProfileEditForm
    template_name = 'users/edit_profile.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, id=request.user.id)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = self.user_instance
        form = UserProfileEditForm(instance=user)
        return render(request, self.template_name, {'user': user, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=self.user_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'edited', extra_tags='success')
        return redirect('users:user_profile')
