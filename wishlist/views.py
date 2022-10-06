from django.shortcuts import render, redirect
from wishlist.models import BarangWishlist
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime

# Create your views here.

def index(request):
    context = {

    }
    return render(request, "index.html", context)

def wishlist_ajax(request):
    context = {
        'nama': 'yancheesetofer',
        'last_login': request.COOKIES['last_login']
    }

    return render(request, "wishlist_ajax.html", context)
    
@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
        'list_barang': data_barang_wishlist,
        'nama': 'yancheesetofer',
        'last_login': request.COOKIES['last_login']
    }
    return render(request, "wishlist.html", context)


def return_xml(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def return_json(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json" )

def return_json_based_on_id(request,id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json" )

def return_xml_based_on_id(request,id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml" )

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response

def create_wishlist(request: HttpRequest):
    if request.method == "POST":
        nama_barang = request.POST.get("nama_barang")
        harga_barang = request.POST.get("harga_barang")
        deskripsi = request.POST.get("deskripsi")

        new_barang = BarangWishlist(
            nama_barang=nama_barang,
            harga_barang=harga_barang,
            deskripsi=deskripsi,
        )
        new_barang.save()
        return HttpResponse(
            serializers.serialize("json", [new_barang]),
            content_type="application/json",
        )

    return HttpResponse("Invalid method", status_code=405)