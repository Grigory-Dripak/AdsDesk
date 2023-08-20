from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

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
    template_name = 'ads_edit.html'
    context_object_name = 'ads'

    def post(self, request, *args, **kwargs):
        ads = Ads(
            category_id=request.POST['category'],
            title=request.POST['title'],
            seller_id=self.request.user.pk,
            content=request.POST['content']
        )
        ads.save()
        return redirect(to=ads.get_absolute_url())


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


class ReplyUpdate(LoginRequiredMixin, UpdateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_edit.html'


class ReplyDelete(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'delete.html'
    success_url = reverse_lazy('ads_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_text'] = 'отклика на публикацию'
        return context


class AdsUpdate(LoginRequiredMixin, UpdateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_edit.html'


class AdsDelete(LoginRequiredMixin, DeleteView):
    model = Ads
    template_name = 'delete.html'
    success_url = reverse_lazy('ads_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_text'] = 'публикации'
        return context