from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.
def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
  return render(request, 'accounts/login.html')

def register(request):
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password2 = request.POST['password2']
    password = request.POST['password']

    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username exists')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email exists')
          return redirect('register')
        else:
          user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
          user.save()
          messages.success(request, 'You ear now registered and can log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')
  return render(request, 'accounts/register.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are logout')
    return redirect('index')

def dashboard(request):
  if not request.user.is_authenticated:
    messages.error('No logged user')
    return redirect('index')
  user_contacts = Contact.objects.filter(user_id=request.user.id).order_by('-contact_date')
  context = {
    'contacts' : user_contacts
  }
  return render(request, 'accounts/dashboard.html', context)