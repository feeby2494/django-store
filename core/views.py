from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from requests import request
from .models import Item, OrderItem, Order


class HomeView(ListView):
    model = Item
    paginate_by = 3
    template_name = "home_page.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order.")
            return redirect('/')


class ItemDetailView(DetailView):
    model = Item
    template_name = "product_page.html"


def service_page(request):

    return render(request, "service_page.html")


def checkout_page(request):

    return render(request, "checkout_page.html")


def user_account(request):

    return render(request, "user_account.html")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_query_set = Order.objects.filter(user=request.user, ordered=False)
    if order_query_set.exists():
        order = order_query_set[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:product_page", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect("core:product_page", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_query_set = Order.objects.filter(user=request.user, ordered=False)
    if order_query_set.exists():
        order = order_query_set[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity:
                order_item.quantity -= 1
                order_item.save()
                return redirect("core:product_page", slug=slug)
            else:
                order.items.remove(order_item)
                messages.info(request, "This item was removed from your cart.")
                return redirect("core:product_page", slug=slug)
        else:
            # Create message that item is not in cart
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product_page", slug=slug)

    else:
        # Create message that user deosn't have an order
        messages.info(request, "You do not have an active order.")
        return redirect("core:product_page", slug=slug)

    return redirect("core:product_page", slug=slug)
