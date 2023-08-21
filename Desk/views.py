from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from .filters import ReplyFilter
from .models import Ads, Emails, Reply
from .forms import AdsForm, CodeForm, ReplyForm
from django.urls import reverse_lazy
from .signals import send_code
from django.contrib.auth.models import Group


class AdsList(ListView):
    model = Ads
    ordering = '-time_creation'
    template_name = 'adslist.html'
    context_object_name = 'ads'
    paginate_by = 10


class MyReplies(LoginRequiredMixin, ListView):
    def get(self, request):
        replies = Reply.objects.filter(reply_to__seller=self.request.user)
        reply_filter = ReplyFilter(request.GET, queryset=replies)
        context = {
            'filter': reply_filter,
        }
        return render(request, 'myreplies.html', context=context)

    # template_name = 'myreplies.html'
    # context_object_name = 'replies'
    # queryset = Reply.objects.all().order_by('-time_creation')
    # paginate_by = 5
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = ReplyFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filterset'] = self.filterset
    #     return context



class AdsDetail(LoginRequiredMixin, DetailView, FormMixin):
    raise_exception = True
    model = Ads
    template_name = 'ads_details.html'
    context_object_name = 'ads_details'
    form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(reply_to_id=self.kwargs['pk']).exclude(status='D')
        context['cur_user_reply']= Reply.objects.filter(
            reply_to_id=self.kwargs['pk'],
            buyer_id=self.request.user.pk
            ).exclude(status='D').exists()
        context['cur_user'] = self.request.user.pk
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user.pk
        ads_pk = self.kwargs['pk']
        ads = Ads.objects.get(pk=ads_pk)
        reply = Reply.objects.create(
            reply_to_id=ads_pk,
            buyer_id=user,
            reply=self.request.POST['reply'],
        )
        reply.save()
        # reply_info.delay(ads_pk)
        return redirect(to=ads.get_absolute_url())


class AdsCreate(PermissionRequiredMixin, CreateView):
    form_class = AdsForm
    model = Ads
    permission_required = ('Desk.add_ads')
    template_name = 'obj_edit.html'
    context_object_name = 'ads'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_text'] = 'Создать публикацию'
        return context

    def post(self, request, *args, **kwargs):
        ads = Ads(
            category_id=request.POST['category'],
            title=request.POST['title'],
            seller_id=self.request.user.pk,
            content=request.POST['content']
        )
        ads.save()
        return redirect(to=ads.get_absolute_url())


class AdsUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    model = Ads
    form_class = AdsForm
    template_name = 'obj_edit.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_text'] = 'Редактирование публикации'
        return context


class AdsDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Ads
    template_name = 'delete.html'
    success_url = reverse_lazy('ads_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_text'] = 'Удаление публикации'
        return context


class ReplyUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    model = Reply
    form_class = ReplyForm
    context_object_name = 'object'
    template_name = 'obj_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_text'] = 'Редактировать отклик'
        return context


class ReplyDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Reply
    template_name = 'delete.html'
    success_url = reverse_lazy('ads_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_text'] = 'Удаление отклика'
        return context


class VerifyEmail(View):
    def get(self, request, *args, **kwargs):
        if Emails.objects.filter(user_id=self.request.user.id, is_verified=False).exists():
            form = CodeForm()
            send_code(user_id=self.request.user.id)
            return render(self.request, 'email_verify.html', {'form': form})
        else:
            return redirect(to='ads_list')

    def post(self, request, *args, **kwargs):
        input_code = int(self.request.POST['activate_code'])
        instance = Emails.objects.get(user_id=self.request.user.id)
        true_code = instance.activate_code
        if input_code == true_code:
            instance.is_verified = True
            instance.save()
            common_users = Group.objects.get(name="common_users")
            common_users.user_set.add(self.request.user)
            return redirect(to='ads_list')
        else:
            form = CodeForm()
            message = 'Неверный код!'
            return render(self.request, 'email_verify.html', {'form': form, 'message': message})
