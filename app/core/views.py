from django.shortcuts import redirect, render
from .models import Concert,QticketsSalesInfo, TargetInfo
from .forms import ConcertForm,SaleForm, TargetForm, SaleCreateForm,TargetCreateForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from . import tasks

# Create your views here.

def home(request):
    context = {

    }
    tasks.add.delay(x = 1, y = 2)
    template = "core/index.html"
    return render(request,template,context)

# def sell(request):
#     context = {
#         list_sell : QticketsSalesInfo.objects.all().order_by("id"),

#     }
    
#     template = "core/sell.html"
#     return render(request,template,context)

def target(request):
    context = {

    }
    
    template = "core/target.html"
    return render(request,template,context)

class CustomSuccessMessage:
    @property
    def success_msg(self):
        return False
    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

# Представления КОНЦЕРТЫ

class ConcertCreateView(CustomSuccessMessage, CreateView):
    model = Concert
    template_name = 'core/concert.html'
    form_class = ConcertForm
    success_url = reverse_lazy('concert')
    success_msg = 'Запись создана'
    def get_context_data(self, **kwargs):
        kwargs['list_concert'] = Concert.objects.all().order_by("id")
        return super().get_context_data(**kwargs)


class ConcertUpdateView(CustomSuccessMessage, UpdateView):
    model = Concert
    template_name = 'core/concert.html'
    form_class = ConcertForm
    success_url = reverse_lazy('concert')
    success_msg = 'Объект обновлен'
    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)


def delete_concert_page(request,pk):
    get_concert = Concert.objects.get(pk = pk)
    get_concert.delete()
    return redirect(reverse('concert'))

# Представления ПРОДАЖИ

class SellCreateView(CustomSuccessMessage, CreateView):
    model = QticketsSalesInfo
    template_name = 'core/sell.html'
    form_class = SaleCreateForm
    success_url = reverse_lazy('sell')
    success_msg = 'Запись создана'
    def get_context_data(self, **kwargs):
        kwargs['list_concert'] = QticketsSalesInfo.objects.all().order_by("id")
        return super().get_context_data(**kwargs)

class SellUpdateView(CustomSuccessMessage, UpdateView):
    model = QticketsSalesInfo
    template_name = 'core/sell.html'
    form_class = SaleForm
    success_url = reverse_lazy('sell')
    success_msg = 'Объект обновлен'
    def get_context_data(self, **kwargs):
        kwargs['account'] = self.object.cat
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

def delete_sell_page(request,pk):
    get_concert = QticketsSalesInfo.objects.get(pk = pk)
    get_concert.delete()
    return redirect(reverse('sell'))

# Представления ТАРГЕТ

# class TargetListView(ListView):
#     model = TargetInfo
#     template_name = "core/target.html"

class TargetCreateView(CustomSuccessMessage, CreateView):
    model = TargetInfo
    template_name = 'core/target.html'
    form_class = TargetCreateForm
    success_url = reverse_lazy('target')
    success_msg = 'Запись создана'
    def get_context_data(self, **kwargs):
        kwargs['list_concert'] = TargetInfo.objects.all().order_by("id")
        return super().get_context_data(**kwargs)

class TargetUpdateView(CustomSuccessMessage, UpdateView):
    model = TargetInfo
    template_name = 'core/target.html'
    form_class = TargetForm
    success_url = reverse_lazy('target')
    success_msg = 'Объект обновлен'
    def get_context_data(self, **kwargs):
        kwargs['account'] = self.object.cat
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

def delete_target_page(request,pk):
    get_concert = TargetInfo.objects.get(pk = pk)
    get_concert.delete()
    return redirect(reverse('target'))