from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse 
from django.shortcuts import get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy

from .models import ShippingAddress
from .forms import ShippingAddressForm

from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView

class ShippingAddressListView(LoginRequiredMixin, ListView):
    login_url = "login"    
    model = ShippingAddress
    template_name = "shipping_addresses/shipping_addresses.html"

    def get_queyset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by("-default")


class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin , UpdateView):
    login_url = "login"
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = "shipping_addresses/update.html"
    success_message = "Dirección actualizada exitosamente"

    def get_success_url(self):
        return reverse("shipping_addresses:shipping_addresses")
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id: 
            return redirect ("carts:cart")
        
        return super (ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)


class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = ShippingAddress
    template_name = "shipping_addresses/delete.html"
    success_url = reverse_lazy("shipping_addresses:shipping_addresses")

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect("shipping_addresses:shipping_addresses")
        
        if request.user.id != self.get_object().user_id: 
            return redirect ("carts:cart")
        
        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url="login")
def create(request):
    
    form = ShippingAddressForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.default = not request.user.has_shipping_address()

        shipping_address.save()


        messages.success(request, "Direccion creada exitosamente")
        return redirect("shipping_addresses:shipping_addresses")

    return render(request, "shipping_addresses/create.html", {
        "form": form
    })

@login_required(login_url="login")
def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect("carts:cart")


    if request.user.has_shipping_address():
        request.user.shipping_address.update_default()

    shipping_address.update_default(True)

    return redirect("shipping_addresses:shipping_addresses")

