from django.shortcuts import render, get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required


def index(request):
    template_data = {}
    for i in range(1, 4):
        cart_total = 0
        movies_in_cart = []
        cart = request.session.get("cart" + str(i), {})
        movie_ids = list(cart.keys())
        if movie_ids != []:
            movies_in_cart = Movie.objects.filter(id__in=movie_ids)
            cart_total = calculate_cart_total(cart, movies_in_cart)
        template_data["movies_in_cart" + str(i)] = movies_in_cart
        template_data["cart" + str(i) + "_total"] = cart_total

    template_data["title"] = "Cart"
    return render(request, "cart/index.html", {"template_data": template_data})


def add(request, id):
    get_object_or_404(Movie, id=id)
    cart_num = request.POST["cartnum"]
    cart = request.session.get("cart" + str(cart_num), {})
    cart[id] = request.POST["quantity"]
    request.session["cart" + str(cart_num)] = cart
    return redirect("cart.index")


def clear(request):
    request.session["cart"] = {}
    return redirect("cart.index")


@login_required
def purchase(request):
    cart = request.session.get("cart", {})
    movie_ids = list(cart.keys())

    if movie_ids == []:
        return redirect("cart.index")

    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()

    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()

    request.session["cart"] = {}
    template_data = {}
    template_data["title"] = "Purchase confirmation"
    template_data["order_id"] = order.id

    return render(request, "cart/purchase.html", {"template_data": template_data})
