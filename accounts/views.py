from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList, ProfileForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PrivacyForm 

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
    
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'],password = request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'

            return render(request, 'accounts/login.html',{'template_data': template_data})

        else:
            auth_login(request,user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        role = request.GET.get('role', None)
        template_data['user_form'] = CustomUserCreationForm()
        if role:
            template_data['profile_form'] = ProfileForm(initial={'role': role})
        else:
            template_data['profile_form'] = ProfileForm()
        template_data['show_candidate_fields'] = (role != 'recruiter')
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            profile = user.profile
            profile.role = profile_form.cleaned_data.get('role', profile.role)
            profile.company = profile_form.cleaned_data.get('company', profile.company)
            profile.headline = profile_form.cleaned_data['headline']
            profile.skills = profile_form.cleaned_data['skills']
            profile.education = profile_form.cleaned_data['education']
            profile.work_experience = profile_form.cleaned_data['work_experience']
            profile.portfolio_link = profile_form.cleaned_data['portfolio_link']
            profile.linkedin_link = profile_form.cleaned_data['linkedin_link']
            profile.github_link = profile_form.cleaned_data['github_link']
            profile.other_links = profile_form.cleaned_data['other_links']
            profile.save()
            
            return redirect('accounts.login')
        else:
            template_data['user_form'] = user_form
            template_data['profile_form'] = profile_form
            posted_role = request.POST.get('role', 'candidate')
            template_data['show_candidate_fields'] = (posted_role != 'recruiter')
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})

@login_required
def privacy_settings(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = PrivacyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            template_data = {'title': 'Privacy Settings', 'form': form, 'success': 'Settings saved!'}
            return render(request, 'accounts/privacy.html', {'template_data': template_data})
    else:
        form = PrivacyForm(instance=profile)
        template_data = {'title': 'Privacy Settings', 'form': form}
    return render(request, 'accounts/privacy.html', {'template_data': template_data})


