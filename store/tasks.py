from ecommerce.celery import app
from django.core.mail import EmailMessage
from django.conf import settings

@app.task
def send_email(user_email,template):

	email = EmailMessage(
	'Thanks for you purchasing!',
	template,
	settings.EMAIL_HOST_USER,
	[user_email],
	)
	email.fail_silently=False
	email.send()
	