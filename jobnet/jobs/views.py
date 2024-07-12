from django.shortcuts import render

# Create your views here.
# jobs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job, Application, Message
from .forms import JobForm, ApplicationForm, MessageForm, ReplyMessageForm

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'jobs/send_message.html', {'form': form})

@login_required
def approve_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user.is_superuser:
        message.approved = True
        message.save()
    return redirect('inbox')

@login_required
def reply_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient = original_message.sender
            reply.is_reply = True
            reply.replied_message = original_message
            reply.save()
            return redirect('inbox')
    else:
        form = ReplyMessageForm()
    return render(request, 'jobs/reply_message.html', {'form': form, 'original_message': original_message})

@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'jobs/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    })
