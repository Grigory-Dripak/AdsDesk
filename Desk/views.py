from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ads, Emails, Reply
from .forms import AdsForm, CodeForm
from django.urls import reverse_lazy
from .signals import send_code
from django.contrib.auth.models import Group

class AdsList(ListView):
    model = Ads
    ordering = '-time_creation'
    template_name = 'adslist.html'
    context_object_name = 'ads'
    paginate_by = 10


# LoginRequiredMixin,
class AdsDetail(PermissionRequiredMixin, DetailView):
    raise_exception = True
    model = Ads
    # queryset = Ads.objects.all()
    template_name = 'ads_details.html'
    context_object_name = 'ads_details'


# PermissionRequiredMixin,
class AdsCreate(PermissionRequiredMixin, CreateView):
    form_class = AdsForm
    model = Ads
    permission_required = ('Ads.add_post',)
    template_name = 'ads_edit.html'
    context_object_name = 'ads'

    def post(self, request, *args, **kwargs):
        # form = AdsForm(request.POST)
        # if not self.request.user.groups.filter(name='virified_email').exists():
        #     form = ...Form()
        #     return redirect(to='verify_email')
        ads = Ads(
            category=request.POST['category'],
            title=request.POST['title'],
            seller=self.request.user,
            content=request.POST['content']
        )
        ads.save()
        return redirect(to='ads_list')


class AdsDelete(DeleteView):
    model = Ads
    # permission_required = ('News.delete_post',)
    template_name = 'ads_delete.html'
    success_url = reverse_lazy('ads_list')


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
