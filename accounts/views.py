from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
def register(req):
    if req.method=="POST":
        form=RegistrationForm(req.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=email.split('@')[0]
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone_number=phone_number
            user.save()
            #account activation code
            current_site=get_current_site(req)
            mail_subject="Please activate your account"
            message=render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            # Important: Email ko HTML batana
            send_mail.content_subtype = "html"
            send_mail.send()
            messages.success(req,"Registration successfully done account activation email send to your register email")
            return redirect('register')
    else:
        form=RegistrationForm()   
    context={
        'form':form
    }
    return render(req,"accounts/register.html",context)


#acount activation logic
def activate(req,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except (TypeError,OverflowError,ValueError,Account.DoesNotExist):
        user=None  
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(req,"your account activated succesfully now able to login") 
        return redirect('login') 
    else:
        messages.error(req,'something went wrong') 
        return redirect('login')   

def forgot_password(req):
    if req.method=="POST":
        email=req.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__iexact=email)
            current_site=get_current_site(req)
            mail_subject="Forgot password"
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            # Important: Email ko HTML batana
            send_mail.content_subtype = "html"
            send_mail.send()
            messages.success(req,'request sent and reset password link sent to your register email')
            return redirect('forgot_password')
        else:
            messages.error(req,"user not found with this email")
            return redirect('forgot_password')
    return render(req,"accounts/forgot_password.html") 


def reset_validate(req,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except (TypeError,OverflowError,ValueError,Account.DoesNotExist):
        user=None  
    if user is not None and default_token_generator.check_token(user,token):
       req.session['uid']=uid
       messages.success(req,'Reset Your Password')
       return redirect('reset_password')
    else:
       messages.error(req,'Invalid link or unAuthorized user!')
       return redirect('forgot_password')


def reset_password(req):
    if req.method=="POST":
        password1=req.POST['password1']
        password2=req.POST['password2']
        if password1==password2:
            uid=req.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password1)
            user.save()
            messages.success(req,'Password reset succesfully')
            return redirect('login')
        else:
            messages.error(req,'password and confirm password should be matched')
            return redirect('reset_password')
    return render(req,'accounts/reset_password.html')


def login(req):
    if req.method=="POST":
        email=req.POST['email']
        password=req.POST['password']
        user=auth.authenticate(email=email,password=password)
        print(user)
        if user is not None:
            auth.login(req,user)
            return redirect("home")
        else:
            messages.error(req,"something wrong credentials")
            return redirect('login')
    return render(req,"accounts/login.html")
@login_required(login_url='login')
def logout_view(req):
    auth.logout(req)
    messages.success(req,"you are logged out")
    return redirect('login')
    