import requests
from .models import Contact
from django.contrib import messages
from django.shortcuts import render, redirect


def contact_view(request):
    if request.method == "POST":
        data = request.POST

        obj = Contact.objects.create(
            name=data.get("name"),
            email=data.get("email"),
            message=data.get("message")
        )
        obj.save()

        token = '7625447889:AAGgo-5ScQts8E4oekIhg__P6p2iNqSgvJA'
        response = requests.get(
            f"https://api.telegram.org/bot{token}/sendMessage?chat_id=5467422443&text="
            f"ASTANA SCHOOL\nid: {obj.id}\nname: {obj.name}\nemail: {obj.email}\nmessage: {obj.message}"
        )

        if response.status_code == 200:
            messages.success(request, "Your message has been sent successfully!")
        else:
            messages.error(request, "It has not been sent successfully, try again later.")

        return redirect("/contact")

    return render(request, 'contact.html', context={'contact': 'active'})
