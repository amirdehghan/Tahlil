from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage


# from .forms import *


from .models import Student
from .tokens import account_activation_token


def login_user(request):
    # TODO get redir from POST/GET
    redirect_to = settings.LOGIN_REDIRECT_URL

    if request.user.is_authenticated:
        return redirect(redirect_to)

    if request.method == 'POST':
        req = request.POST
        user = authenticate(username=req['username'], password=req['password'])
        if not user:
            return render(request,'authentication/login.html',{'error_message': 'Wrong password'})
        else:
            login(request, user)
            return redirect(redirect_to)

    return render(request,'authentication/login.html',{})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def signup_user(request):
    # TODO get redir from POST/GET
    redirect_to = settings.LOGIN_REDIRECT_URL

    if request.user.is_authenticated:
        return redirect(redirect_to)

    if request.method == 'POST':
        # TODO make user is_active=False, then send activation email
        # form = StudentSignUpForm(request.POST)
        # if(form.is_valid()):
        #     print(1)
        #     form.save()
        #     return render(request, 'authentication/signup/verification.html',
        #                   {'message': 'Your account was successfully created.', 'type': 'success'})
        # print(2)
        ####
        user = User(username='s_' + request.POST['student_id'])
        user.set_password(request.POST['password'])
        user.save()
        user.is_active = False
        student = Student(user=user, student_id=request.POST['student_id'])
        student.save()

        print(1)
        current_site = get_current_site(request)
        print(2)
        mail_subject = 'Activate your blog account.'
        # print(current_site.domain)
        tk = account_activation_token.make_token(student.user)
        print(user)
        message = render_to_string('acc_active_email.html', {
            'user': request.POST['student_id'],
            'pk':request.POST['student_id'],
            'token':tk,
        })
        print(3)
        to_email = request.POST['email']
        print(4)
        print(to_email)
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()





        # login(request, user)
        return render(request, 'authentication/signup/verification.html', \
            {'message' : 'Your account was successfully created.', 'type' : 'success'})



    return render(request,'authentication/signup/signup.html',{})

def activate(request, uid, token):
    try:
        user = Student.objects.get(pk=uid).user
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print(user)
    # tk = account_activation_token.make_token(user)
    print(account_activation_token.check_token(user, token))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
