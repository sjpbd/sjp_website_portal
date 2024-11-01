from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.mail import EmailMessage
from .models import AppointmentLetter, Notification
from .forms import AppointmentLetterForm
import os
from django.utils import timezone

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class AppointmentLetterListView(AdminRequiredMixin, ListView):
    model = AppointmentLetter
    template_name = 'appointments/letter_list.html'
    context_object_name = 'letters'
    paginate_by = 10

class AppointmentLetterDetailView(AdminRequiredMixin, DetailView):
    model = AppointmentLetter
    template_name = 'appointments/letter_detail.html'
    context_object_name = 'letter'

class AppointmentLetterCreateView(AdminRequiredMixin, CreateView):
    model = AppointmentLetter
    form_class = AppointmentLetterForm
    template_name = 'appointments/letter_form.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def generate_pdf(request, pk):
    """
    Generate PDF from the appointment letter details.
    """
    letter = get_object_or_404(AppointmentLetter, pk=pk)
    html_string = render_to_string('appointments/pdf_template.html', {'letter': letter})

    # Log the HTML content to verify it contains the expected data
    print("Generated HTML for PDF:", html_string)

    # Generate PDF using WeasyPrint
    try:
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        # Log if the PDF generation is successful
        print("PDF generation successful")

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="appointment_letter_{letter.reference_number}.pdf"'
        return response

    except Exception as e:
        # Log the exception details for debugging
        print(f"Error generating PDF: {e}")
        messages.error(request, 'An error occurred while generating the PDF.')
        return redirect('appointments:letter_detail', pk=pk)


def send_letter(request, pk):
    """
    Send appointment letter as an email with the PDF attached.
    """
    letter = get_object_or_404(AppointmentLetter, pk=pk)
    
    # Create notification for the user
    Notification.objects.create(
        user=letter.user,
        appointment_letter=letter
    )
    
    # Update letter status to 'sent' and record the sent date
    letter.status = 'sent'
    letter.sent_date = timezone.now()
    letter.save()
    
    # Generate PDF for the email attachment
    html_string = render_to_string('appointments/pdf_template.html', {'letter': letter})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Email configuration
    subject = f"Your Appointment Letter - {letter.reference_number}"
    message = f"Dear {letter.user.first_name},\n\nPlease find attached your official appointment letter."
    email = EmailMessage(
        subject,
        message,
        'from@example.com',  # Replace with your "from" email
        [letter.user.email],  # Email to the user
    )
    
    # Attach PDF to the email
    email.attach(f"appointment_letter_{letter.reference_number}.pdf", pdf, 'application/pdf')
    
    try:
        email.send()
        messages.success(request, 'Appointment letter sent successfully!')
    except Exception as e:
        messages.error(request, 'There was an error sending the email. Please try again.')
    
    return redirect('appointments:letter_list')

