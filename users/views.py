import requests
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, FormView, View

# local import
from users.models import User
from users.forms import UserProfileForm, PersonalDetailsForm, UserLoginForm



# Create your views here.


class LoginRequiredMixin(View):
    """
    View mixin which verifies that the user has authenticated..
    """
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("users:login")
        return super().dispatch(request, *args, **kwargs)


class HomePageView(TemplateView):
    """
        - Home page view with TemplateView
    """
    template_name="base.html"


class UserListView(ListView, LoginRequiredMixin):
    """
        - User List View used for showing list of users
        with paggination.
        - currently I Have added paginated_by 2 only you can change whatever you want
        - get queryset method will for returning list of all users with order_by "created at" date
    """
    model = User
    paginate_by = 2
    template_name= "users/user-list.html"
    context_object_name = "users"

    def get_queryset(self):
        queryset = User.objects.all().order_by('-created_at')
        return queryset


class UserRegistrationView(CreateView):
    """
        - User can Registeration from here
        - get_context_data method will be used for adding extra context data for my template
        - form_valid method will be called when User form have all correct fileds
        - for getting gender detial i have implemented of genderize api
        - for genrating random passoword and send to user email i have used make_random_password
          and send_mail django default email send fucntion
        - form_invalid method will be called when User filled invalid data in filed
    """
    model = User
    form_class = UserProfileForm
    personal_detail_form = PersonalDetailsForm
    template_name = "users/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form1"] = self.personal_detail_form
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        param = {"name": obj.first_name}
        gender_api = "https://api.genderize.io/"
        resp = requests.get(gender_api, params=param)
        resp_json_data = resp.json()
        if resp_json_data['gender'] == "male":
            gender = "M"
        elif  resp_json_data['gender'] == "female":
            gender = "F"
        else:
            gender = "O"
        obj.gender = gender
        radom_password = User.objects.make_random_password()
        obj.set_password(radom_password)
        print("-------------------------------------------------")
        print(radom_password)
        mail_from = getattr(settings, "EMAIL_HOST_USER", "")
        mail_subject = "Your randome password genrated for ThinkTanker system."
        message_body = f"Your password is :{radom_password}"
        send_mail(
                mail_subject,
                "",
                mail_from,
                [obj.email],
                html_message=message_body,
                fail_silently=False,
            )
        print("-------------------------------------------------")
        obj.save()

        # Save hobbies
        form1 = PersonalDetailsForm(self.request.POST)
        if form1.is_valid():
            obj1 = form1.save(commit = False)
            age_count = datetime.date.today().year - obj.date_of_birth.year
            obj1.user = obj
            selected_hobbies = form1.cleaned_data['hobbies']
            obj1.age = age_count
            obj1.save()
            obj1.hobbies.add(*selected_hobbies)
            obj1.save()

        return redirect("users:user_list")

    def form_invalid(self, form):
        messages.error(self.request, "Please Enter valid details")
        return super().form_invalid(form)


class UserLoginView(FormView):
    """
        Used to manage User Login view
    """
    form_class = UserLoginForm
    template_name = "users/login.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("users:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.cleaned_data
        login(self.request, user)
        messages.success(self.request,f"{user.email} Logged In Sucessfully.")
        return redirect("users:home")

    def form_invalid(self, form):
        return super().form_invalid(form)

class UserLogoutView(View):
    """
        - User logout view
    """
    def get(self,request, *args, **kwargs):
        logout(request)
        return redirect("users:login")
