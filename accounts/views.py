from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList, ProfileForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PrivacyForm 
from .models import Profile, Job, Recommendation
from helpers import parse_skills_string, is_match
from profiles.models import Message
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.models import User

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
            # Save free-text location provided at signup (if any)
            profile.location = profile_form.cleaned_data.get('location', profile.location)
            profile.save()
            Profile.objects.get_or_create(user = user, privacy = 'public', role = profile.role, company = profile.company,
                                          headline = profile.headline, 
                                          skills = profile.skills, 
                                          education = profile.education,
                                          work_experience = profile.work_experience,
                                          portfolio_link = profile.portfolio_link,
                                          linkedin_link = profile.linkedin_link, 
                                          github_link = profile.github_link,
                                          other_links = profile.other_links,
                                          location = profile.location)
            #if there is a match - this is a new match
            # notify the recruiter in the portal via Messages tab
            if profile.role == 'candidate':  # When job seeker gets added:
                recruiters_only_dummy_user, is_successful = User.objects.get_or_create(username="recruiter_notification")
                for job in Job.objects.all():  # loop through each job
                    if is_match(profile, job):
                        Recommendation.objects.get_or_create(profile=profile, job=job)  # create recommendation
                        all_users = User.objects.all()
                        if job.savedCandidateSearch == True:
                            subject = "New Match Notification"
                            body = "We found a new match! Job: ", job, " Candidate Match: ", request.POST.get('username')
                            Message.objects.create(sender=user, recipient=recruiters_only_dummy_user, subject=subject, body=body)
        
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


@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    """Display a simple admin page listing users and their roles. Superuser-only."""
    users = User.objects.select_related('profile').all().order_by('username')
    return render(request, 'accounts/manage_users.html', {'users': users, 'template_data': {'title': 'Manage Users'}})


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def update_user_role(request):
    """Handle AJAX or form POST to update a user's profile.role.

    Expects POST data: user_id, role (one of candidate|recruiter).
    Returns JSON with success flag and new role.
    """
    user_id = request.POST.get('user_id')
    new_role = request.POST.get('role')
    if not user_id or new_role not in dict(Profile.ROLE_CHOICES).keys():
        return JsonResponse({'success': False, 'error': 'Invalid input'}, status=400)
    try:
        user = User.objects.get(id=int(user_id))
        profile = user.profile
        profile.role = new_role
        profile.save()
        messages.success(request, f"Updated role for {user.username} to {new_role}")
        return JsonResponse({'success': True, 'user_id': user_id, 'new_role': new_role})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def toggle_user_active(request):
    """Toggle a user's is_active flag. POST: user_id, active ('true'|'false')"""
    user_id = request.POST.get('user_id')
    active = request.POST.get('active')
    if not user_id or active not in ['true', 'false']:
        return JsonResponse({'success': False, 'error': 'Invalid input'}, status=400)
    try:
        user = User.objects.get(id=int(user_id))
        user.is_active = (active == 'true')
        user.save()
        return JsonResponse({'success': True, 'user_id': user_id, 'is_active': user.is_active})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def toggle_user_staff(request):
    """Toggle a user's is_staff flag. POST: user_id, staff ('true'|'false')"""
    user_id = request.POST.get('user_id')
    staff = request.POST.get('staff')
    if not user_id or staff not in ['true', 'false']:
        return JsonResponse({'success': False, 'error': 'Invalid input'}, status=400)
    try:
        user = User.objects.get(id=int(user_id))
        user.is_staff = (staff == 'true')
        user.save()
        return JsonResponse({'success': True, 'user_id': user_id, 'is_staff': user.is_staff})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


