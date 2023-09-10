from django.contrib.auth import (
    login,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import atomic
from django.shortcuts import (render, redirect, )
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import (
    TemplateView, FormView,
)

from accounts.forms import SignupForm, LoginForm
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView,
)


# Create your views here.
class SignupView(View):
    template_name = "accounts/registration.html"

    def get(self, request):
        """
        Provides the registration form.
        """
        context = {}
        form = SignupForm()
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Validates data and creates new user.
        """
        context = {}
        form = SignupForm(request.POST)

        if form.is_valid():
            with atomic():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                login(request, user)
            return redirect(reverse("accounts:profile"))
        else:
            context["form"] = form
            return render(request, self.template_name, context)


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(reverse('accounts:profile'))

        return super().dispatch(request, *args, **kwargs)


class LoginView(GuestOnlyView, FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # if settings.USE_REMEMBER_ME:
        #     if not form.cleaned_data['remember_me']:
        #         request.session.set_expiry(0)

        login(request, form.user_cache)

        return redirect(reverse('accounts:profile'))


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'accounts/logout.html'
