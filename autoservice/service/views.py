from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from .forms import AppointmentForm
from django.contrib.auth import logout
from .models import Service, Appointment


def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    services_count = Service.objects.count()
    appointments_count = Appointment.objects.count()
    context = {
        'services_count': services_count,
        'appointments_count': appointments_count,
    }
    return render(request, 'index.html', context)

class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'

@login_required
def appointment_create(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.service = service
            appointment.user = request.user
            appointment.status = 'pending'
            appointment.save()
            return redirect('index')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointment_form.html', {'service': service, 'form': form})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'