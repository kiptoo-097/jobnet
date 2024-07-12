from django.urls import path
from .views import post_job, apply_job, send_message, approve_message, reply_message

urlpatterns = [
    path('post/', post_job, name='post_job'),
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('send_message/', send_message, name='send_message'),
    path('approve_message/<int:message_id>/', approve_message, name='approve_message'),
    path('reply_message/<int:message_id>/', reply_message, name='reply_message'),
]