from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q, Count

from .models import Application
from accounts.models import Profile
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Message
from .forms import MessageForm, EmailForm
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

@login_required
def my_applications(request):
    apps = (
        Application.objects
        .select_related("job")
        .filter(candidate=request.user)
        .order_by("-updated_at")
    )
    return render(request, "my_applications.html", {"apps": apps})
def candidate_search(request):
    term = request.GET.get('q', '').strip()

    is_recruiter = False
    if request.user.is_authenticated:
        try:
            is_recruiter = request.user.profile.role == 'recruiter'
        except Exception:
            is_recruiter = False

    if is_recruiter:
        qs = Profile.objects.select_related('user').filter(role='candidate').filter(
            Q(privacy='public') | Q(privacy='recruiters')
        )
    else:
        qs = Profile.objects.select_related('user').filter(role='candidate', privacy='public')

    if term:
        qs = qs.filter(
            Q(user__username__icontains=term) |
            Q(headline__icontains=term) |
            Q(skills__icontains=term) |
            Q(education__icontains=term) |
            Q(work_experience__icontains=term)
        )

    return render(request, 'candidate_search.html', {'candidates': qs, 'is_recruiter': is_recruiter})


@login_required
def inbox(request):
    # Get messages for the current user, ordered by newest first
    msgs = Message.objects.filter(recipient=request.user)\
        .select_related('sender')\
        .order_by('-created_at')\
        .distinct('created_at', 'sender')\
        .values('id', 'sender', 'subject', 'body', 'created_at', 'sender__username')\
        .distinct()
    
    return render(request, 'message_inbox.html', {
        'message_list': msgs,  # Renamed to avoid conflict with Django's messages framework
        'title': 'Messages'
    })


@login_required
def compose_message(request, recipient_id=None):
    # Only recruiters can compose internal messages to candidates
    try:
        user_profile = request.user.profile
    except Exception:
        user_profile = None
    if not user_profile or user_profile.role != 'recruiter':
        messages.error(request, 'Only recruiters can send internal messages.')
        return redirect('profiles:candidate_search')
    User = get_user_model()
    initial = {}
    if recipient_id:
        recipient = get_object_or_404(User, pk=recipient_id)
        initial['recipient_id'] = recipient.id
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            rid = form.cleaned_data['recipient_id']
            recipient = get_object_or_404(User, pk=rid)
            # Only allow messaging actual candidates
            if getattr(recipient, 'profile', None) and recipient.profile.role != 'candidate':
                messages.error(request, 'You can only message candidates.')
                return redirect('profiles:candidate_search')
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            Message.objects.create(sender=request.user, recipient=recipient, subject=subject, body=body)
            messages.success(request, 'Message sent to {}.'.format(recipient.username))
            return redirect('profiles:candidate_search')
    else:
        form = MessageForm(initial=initial)
    return render(request, 'compose_message.html', {'form': form})


@login_required
def compose_email(request, recipient_id=None):
    # Only recruiters can send emails through the platform
    try:
        user_profile = request.user.profile
    except Exception:
        user_profile = None
    if not user_profile or user_profile.role != 'recruiter':
        messages.error(request, 'Only recruiters can send emails to candidates.')
        return redirect('profiles:candidate_search')
    User = get_user_model()
    recipient_email = ''
    if recipient_id:
        recipient = get_object_or_404(User, pk=recipient_id)
        recipient_email = getattr(recipient, 'email', '')
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            to = form.cleaned_data['recipient_email']
            users_with_email = list(User.objects.filter(email=to))
            candidate_users = [u for u in users_with_email if getattr(u, 'profile', None) and u.profile.role == 'candidate']
            if len(candidate_users) == 1:
                user_with_email = candidate_users[0]
            elif len(candidate_users) > 1:
                messages.error(request, 'Multiple candidate accounts found for that email address. Please select the candidate from the search results and send the email from their profile.')
                return redirect('profiles:candidate_search')
            else:
                messages.error(request, 'Emails may only be sent to registered job seekers via their account. Please select a candidate from search.')
                return redirect('profiles:candidate_search')
            subject = settings.EMAIL_SUBJECT_PREFIX + (form.cleaned_data['subject'] or '(no subject)')
            # Add recruiter information to the body
            recruiter_info = f"\n\n---\nThis message was sent by {request.user.username}"
            if request.user.email:
                recruiter_info += f"\nTo reply directly: {request.user.email}"
            if request.user.profile.company:
                recruiter_info += f"\nCompany: {request.user.profile.company}"
            body = form.cleaned_data['body'] + recruiter_info
            
            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[to],
                    fail_silently=False
                )
                messages.success(request, f'Email sent successfully to {to}.')
            except BadHeaderError:
                messages.error(request, 'Invalid header found in email. Please check the subject.')
            except ConnectionRefusedError:
                messages.error(request, 'Could not connect to email server. Please try again later.')
            except Exception as e:
                if 'Authentication' in str(e):
                    messages.error(request, 'Email authentication failed. Please contact system administrator.')
                else:
                    messages.error(request, f'Failed to send email: {e}')
            return redirect('profiles:candidate_search')
    else:
        form = EmailForm(initial={'recipient_email': recipient_email})
    return render(request, 'compose_email.html', {'form': form})
