import logging

from django.shortcuts import redirect, render
from django.views import View
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

from django.conf import settings

logger = logging.getLogger(__name__)


class Landing(View):
    template_name = 'pages/landing.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """Handle the contact form submission on the landing page."""
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, email, message]):
            messages.error(request, 'All fields are required. Please fill in the form completely.')
            return redirect('pages:landing')

        subject = f"New contact message from: {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        if not settings.EMAIL_HOST_USER:
            logger.warning('Contact form submitted but EMAIL_HOST_USER is not configured.')
            messages.error(request, 'Email service is not configured. Please contact the administrator.')
            return redirect('pages:landing')

        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ['smartweb801@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except BadHeaderError:
            logger.exception('Invalid header in contact form submission.')
            messages.error(request, 'Invalid form data. Please try again.')
        except Exception:
            logger.exception('Failed to send contact form email.')
            messages.error(request, 'An error occurred while sending the message. Please try again later.')

        return redirect('pages:landing')