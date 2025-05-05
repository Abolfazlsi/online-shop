from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, View, ListView, CreateView
from product.models import Product, Rating, Comment, Category, ContactUs
from django.urls import reverse_lazy
from .forms import ContactUsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from product.filter_products import products_filter


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product_detail.html"

    def post(self, request, slug):
        text = request.POST.get("text")
        product = get_object_or_404(Product, slug=slug)
        if request.user.is_authenticated:
            add_comment = Comment.objects.create(user=request.user, text=text, product=product)
            return JsonResponse({
                "status": "success",
                "comment_text": add_comment.text,
                "user_username": add_comment.user.fullname if add_comment.user.fullname else add_comment.user.phone,
                "created_at": add_comment.time_since_creation(),
                'slug': product.slug
            })

    def get_related_products(self, product):
        categories = product.category.all()

        related_products = Product.objects.filter(category__in=categories).exclude(slug=product.slug)[:12]
        return related_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        context['related_products'] = self.get_related_products(product)

        if self.request.user.is_authenticated:
            if self.request.user.ratings.filter(product=self.object, user=self.request.user).exists():
                context["is_rate"] = True
            else:
                context["is_rate"] = False

        return context


class RatingsView(LoginRequiredMixin, View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        try:
            rating = Rating.objects.get(product=product, user=request.user)
            rating.delete()
            return JsonResponse({"response": "on_rating"})
        except:
            Rating.objects.create(product=product, user=request.user)
            return JsonResponse({"response": "rating"})


class ProductsListView(ListView):
    model = Product
    template_name = "product/products_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context.update(products_filter(self.request, products))

        return context


class SearchProductView(ListView):
    model = Product
    template_name = "product/products_list.html"

    def get_queryset(self):
        q = self.request.GET.get("q")
        return Product.objects.filter(name__icontains=q) if q else Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        context.update(products_filter(self.request, products))

        return context


class CategoryDetailView(ListView):
    model = Category
    template_name = "product/products_list.html"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Product.objects.filter(category__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        context.update(products_filter(self.request, products))

        return context


class ContactUsView(CreateView):
    model = ContactUs
    form_class = ContactUsForm
    template_name = "product/contact_us.html"
    success_url = reverse_lazy("product:contact_us")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(ContactUsView, self).form_valid(form)
