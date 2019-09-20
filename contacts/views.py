from django.shortcuts import render, redirect
from django.contrib import messages
from contacts.models import Contact

# Create your views here.
def contact(request):
  if request.method == 'POST':
    listing_id = request.POST['listing_id']
    listing = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    user_id = request.POST['user_id']
    phone = request.POST['phone']

    if request.user.is_authenticated:
        user_id = request.user.id
        has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
        if has_contacted:
            messages.error(request, 'You have alreay made inquire')
            return redirect('/listings/' + listing_id)

    contact = Contact(listing_id=listing_id, listing=listing, name=name, email=email, 
                      message=message, user_id=user_id, phone=phone)
    contact.save()

    messages.success(request, 'Your request was submitted')
    return redirect('/listings/' + listing_id)