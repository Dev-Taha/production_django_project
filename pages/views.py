from django.shortcuts import render, redirect
from django.views import generic
from django.core.mail import send_mail
from django.contrib import messages


class Landing(generic.TemplateView):
    template_name = 'pages/landing.html'

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

        try:
            send_mail(
                subject,
                full_message,
                email,
                ['smartweb801@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception:
            messages.error(request, 'An error occurred while sending the message. Please try again.')

        return redirect('pages:landing')