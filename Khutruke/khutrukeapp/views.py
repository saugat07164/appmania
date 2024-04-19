<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Item
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ItemForm

def home_view(request):
    return render(request, 'home.html')

from django.http import HttpResponseRedirect

class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'items'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') # Redirect to the login page
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        for item in queryset:
            # Calculate duration in days
            duration = (timezone.now() - item.uploaded_at).days
            # Calculate interest based on interest rate per day
            interest = (item.deposit * item.interest_rate / 100) * duration
            # Calculate total deposit including interest
            total_deposit = item.deposit + interest
            item.total_deposit = total_deposit
            item.progress_percentage = (total_deposit / item.price) * 100
        return queryset

    def post(self, request, *args, **kwargs):
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.uploader = request.user # Set the uploader as the current authenticated user
            item.save()
            return HttpResponseRedirect(request.path) # Redirect to the same page after successful form submission
        else:
            # If form is not valid, render the item list page with the form and items
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemForm() # Add the ItemForm instance to the context
        return context

    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        duration = (timezone.now() - item.uploaded_at).days
        interest = (item.deposit * item.interest_rate / 100) * duration
        total_deposit = item.deposit + interest
        if item.price != 0:
            progress_percentage = (total_deposit / item.price) * 100
        else:
            progress_percentage = 0
        context['item_id'] = self.get_object().id 
        context['progress_percentage'] = progress_percentage
        return context


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_view')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def about_view(request):
    return render(request, 'about.html')
def contact_view(request):
    return render(request, 'contact.html')
=======
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Item
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ItemForm

def home_view(request):
    return render(request, 'home.html')

from django.http import HttpResponseRedirect

class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'items'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') # Redirect to the login page
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        for item in queryset:
            # Calculate duration in days
            duration = (timezone.now() - item.uploaded_at).days
            # Calculate interest based on interest rate per day
            interest = (item.deposit * item.interest_rate / 100) * duration
            # Calculate total deposit including interest
            total_deposit = item.deposit + interest
            item.total_deposit = total_deposit
            item.progress_percentage = (total_deposit / item.price) * 100
        return queryset

    def post(self, request, *args, **kwargs):
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.uploader = request.user # Set the uploader as the current authenticated user
            item.save()
            return HttpResponseRedirect(request.path) # Redirect to the same page after successful form submission
        else:
            # If form is not valid, render the item list page with the form and items
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemForm() # Add the ItemForm instance to the context
        return context

    
class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'item_detail.html'
    context_object_name = 'item'  # Change context_object_name to 'item'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_view')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
>>>>>>> 56e8ba141c7ecebe8811d153cbf7b97be881f469
