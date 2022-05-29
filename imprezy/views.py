from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import NewUserForm, AddPartyForm, GiftForm
from .models import Party, Gift
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def homepage(request):
    return render(request=request, template_name='homepage.html')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Rejestracja przebiegła pomyślnie")
            return redirect("homepage")
        else:
            messages.error(request, "Rejestracja nie powiodła się. Podano błędne informacje.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Jesteś zalogowany jako {username}.")
                return redirect("homepage")
            else:
                messages.error(request, "Wprowadzono złą nazwę użytkownika lub hasło.")
        else:
            messages.error(request, "Wprowadzono złą nazwę użytkownika lub hasło.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Wylogowano się poprawnie.")
    return redirect("homepage")

class AddParty(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request):
        form = AddPartyForm()
        return render(request, 'addParty.html', {'form':form})

    def post(self, request):
        form = AddPartyForm(request.POST)
        if form.is_valid():
            party_name = form.cleaned_data['party_name']
            party_date = form.cleaned_data['party_date']
            party_time = form.cleaned_data['party_time']
            description = form.cleaned_data['description']
            user = request.user
            Party.objects.create(party_name=party_name, party_date=party_date, party_time=party_time, description=description, user=user)
            return redirect("party-list")
        else:
            return render(request, 'addParty.html', {'form': form})


class PartiesListView(LoginRequiredMixin, View):
    login_url = "/login"
    def get(self, request):
        parties = Party.objects.all()
        return render(request, "parties.html", context={"parties": parties})


class AddGift(View):
    def get(self, request):
        form = GiftForm()
        return render(request, 'gifts.html', {'form':form})

    def post(self, request):
        form = GiftForm(request.POST)
        if form.is_valid():
            gift_name = form.cleaned_data['gift_name']
            gift_link = form.cleaned_data['gift_link']
            comments = form.cleaned_data['comments']
            gift = Gift.objects.create(gift_name=gift_name)
            return redirect("gift-list", gift_id=gift.id)
        else:
            return render(request, 'gifts.html', {'form': form})

class DeletePartyView(View):
    def get(self, request, party_id):
        party = Party.objects.get(id=party_id)
        party.delete()
        return redirect("party-list")


