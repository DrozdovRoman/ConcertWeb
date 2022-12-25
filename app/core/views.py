from django.shortcuts import redirect, render
from .models import Concert,QticketsSalesInfo, TargetInfo
from .forms import ConcertForm,SaleForm, TargetForm, SaleCreateForm,TargetCreateForm,AuthUserForm,RegisterUserForm
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, View
from django.contrib import messages
from . import tasks
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .functions.SetInfoOneDate import SetInfoOneDate
from .functions.GoogleSheetsFunctions.CreateTemplate import CreateConcertTemplateSellTable, UpdateConcertTemplateSellTable,ClearConcertTemplateSellTable, CreateConnectQticketsAccount, ChangeConnectQticketsAccount, ClearConnectQticketsAccount, CreateConnectTargetAccount, ChangeConnectTargetAccount, ClearConcertTemplateTargetTable
from datetime import datetime

# Create your views here.

def home(request):
    context = {

    }
    # tasks.add.delay(x = 1, y = 2)
    template = "core/index.html"
    return render(request,template,context)

# def sell(request):
#     context = {
#         list_sell : QticketsSalesInfo.objects.all().order_by("id"),

#     }
    
#     template = "core/sell.html"
#     return render(request,template,context)

# def target(request):
#     context = {

#     }
    
#     template = "core/target.html"
#     return render(request,template,context)

class CustomSuccessMessage:
    @property
    def success_msg(self):
        return False
    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

# Представления КОНЦЕРТЫ

class ConcertCreateView(LoginRequiredMixin, CustomSuccessMessage, CreateView):
    login_url = 'login_page'
    model = Concert
    template_name = 'core/concert.html'
    form_class = ConcertForm
    success_url = reverse_lazy('concert')
    success_msg = 'Запись создана'
    def get_context_data(self, **kwargs):
        kwargs['list_concert'] = Concert.objects.all().order_by("id")
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # Закрепление за авторизированным пользователем текущей статьи
        self.object = form.save(commit = False)
        self.object.author = self.request.user

                # Создание шаблона в GoogleSheet пользователя
        spreadSheetPosition = CreateConcertTemplateSellTable(
            form.cleaned_data['name'],
            form.cleaned_data['city'],
            form.cleaned_data['concert_date']
            )
        self.object.spreadSheetPositon = spreadSheetPosition
        self.object.save()
        return super().form_valid(form)


class ConcertUpdateView(LoginRequiredMixin, CustomSuccessMessage, UpdateView):
    login_url = 'login_page'
    model = Concert
    template_name = 'core/concert.html'
    form_class = ConcertForm
    success_url = reverse_lazy('concert')
    success_msg = 'Объект обновлен'

    def form_valid(self, form):
        UpdateConcertTemplateSellTable (
            form.cleaned_data['name'],
            form.cleaned_data['city'],
            form.cleaned_data['concert_date'],
            form.cleaned_data['spreadSheetPositon']
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self): # Проверка прав доступа к таблице
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
                return self.handle_no_permission()
        return kwargs

class ConcertDeleteView(LoginRequiredMixin, CustomSuccessMessage, DeleteView):
    model = Concert
    template_name='core/delete_view.html'
    success_url=reverse_lazy('concert')
    success_msg = 'Запись удалена'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        ClearConcertTemplateSellTable(self.object.spreadSheetPositon)
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

# def delete_concert_page(request,pk):
#     get_concert = Concert.objects.get(pk = pk)
#     get_concert.delete()
#     return redirect(reverse('concert'))

# Представления ПРОДАЖИ

class SellCreateView(LoginRequiredMixin, CustomSuccessMessage, CreateView):
    login_url = 'login_page'
    model = QticketsSalesInfo
    template_name = 'core/sell.html'
    form_class = SaleCreateForm
    success_url = reverse_lazy('sell')
    success_msg = 'Запись создана'
    def get_context_data(self, **kwargs):
        kwargs['list_concert'] = QticketsSalesInfo.objects.all().order_by("id")
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        self.object = form.save(commit = False)
        spreadSheetQticketsPosition = CreateConnectQticketsAccount(
        form.cleaned_data['qticketsConcertID'],
        form.cleaned_data['cat'].spreadSheetPositon)
        self.object.spreadSheetQticketsPosition = spreadSheetQticketsPosition
        self.object.save()
        return super().form_valid(form)

class SellUpdateView(LoginRequiredMixin, CustomSuccessMessage, UpdateView):
    login_url = 'login_page'
    model = QticketsSalesInfo
    template_name = 'core/sell.html'
    form_class = SaleForm
    success_url = reverse_lazy('sell')
    success_msg = 'Объект обновлен'
    def get_context_data(self, **kwargs):
        kwargs['account'] = self.object.cat
        kwargs['update'] = True
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        ChangeConnectQticketsAccount(
            form.cleaned_data['qticketsConcertID'],
            self.object.cat.spreadSheetPositon,
            form.cleaned_data['spreadSheetQticketsPosition']
        )
        return super().form_valid(form)

class SellDeleteView(LoginRequiredMixin, CustomSuccessMessage, DeleteView):
    model = QticketsSalesInfo
    template_name='core/delete_view.html'
    success_url=reverse_lazy('sell')
    success_msg = 'Запись удалена'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.cat.author:
            return self.handle_no_permission()
        ClearConnectQticketsAccount(
            self.object.cat.spreadSheetPositon,
            self.object.spreadSheetQticketsPosition
        )
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

# Представления ТАРГЕТ

class TargetCreateView(LoginRequiredMixin, CustomSuccessMessage, CreateView):
    login_url = 'login_page'
    model = TargetInfo
    template_name = 'core/target.html'
    form_class = TargetCreateForm
    success_url = reverse_lazy('target')
    success_msg = 'Запись создана'
    def get_context_data(self, **kwargs):
        kwargs['list_concert'] = TargetInfo.objects.all().order_by("id")
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit = False)
        spreadSheetTargetPosition = CreateConnectTargetAccount(
        form.cleaned_data['targetCompanyID'],
        form.cleaned_data['cat'].spreadSheetPositon)
        self.object.spreadSheetTargetPosition = spreadSheetTargetPosition
        self.object.save()
        return super().form_valid(form)

class TargetUpdateView(LoginRequiredMixin, CustomSuccessMessage, UpdateView):
    login_url = 'login_page'
    model = TargetInfo
    template_name = 'core/target.html'
    form_class = TargetForm
    success_url = reverse_lazy('target')
    success_msg = 'Объект обновлен'
    def get_context_data(self, **kwargs):
        kwargs['account'] = self.object.cat
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        ChangeConnectTargetAccount(
            form.cleaned_data['targetCompanyID'],
            self.object.cat.spreadSheetPositon,
            self.object.spreadSheetTargetPosition
        )
        return super().form_valid(form)


class TargetDeleteView(LoginRequiredMixin, CustomSuccessMessage, DeleteView):
    model = TargetInfo
    template_name='core/delete_view.html'
    success_url=reverse_lazy('target')
    success_msg = 'Запись удалена'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.cat.author:
            return self.handle_no_permission()
        ClearConcertTemplateTargetTable(
            self.object.targetCompanyID,
            self.object.cat.spreadSheetPositon,
            self.object.spreadSheetTargetPosition
        )
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

# def delete_target_page(request,pk):
#     get_concert = TargetInfo.objects.get(pk = pk)
#     get_concert.delete()
    # return redirect(reverse('target'))


# Управление технической таблицы

class ControlPanelPage(LoginRequiredMixin,View):
    login_url = 'login_page'
    template_name = "core/control_panel.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

def TestUpdate(request):
    day_update = request.GET.get("day_update")
    day_update = datetime.strptime(day_update, "%Y-%m-%d")
    
    target_info = list(TargetInfo.objects.values())
    qticketsSales_info = list(QticketsSalesInfo.objects.values())
    concert_info = list(Concert.objects.values())
    SetInfoOneDate(target_info, qticketsSales_info, concert_info, day_update)
    template = "core/control_panel.html"
    context = {}
    return render(request,template,context)


# Представления авторизация

class UserLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')
    def get_success_url(self):
        return self.success_url

class UserRegisterView(CreateView):
    model = User
    template_name = 'core/register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    success_msg = 'Пользователь успешно создан'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username = username, password = password)
        login(self.request, auth_user)
        return form_valid

class UserLogout(LogoutView):
    next_page = reverse_lazy('home')