from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ads
from .forms import AdsForm
from django.urls import reverse_lazy


class AdsList(ListView):
    model = Ads
    ordering = '-time_creation'
    template_name = 'adslist.html'
    context_object_name = 'ads'
    paginate_by = 10


# LoginRequiredMixin,
class AdsDetail(DetailView):
    # raise_exception = True
    model = Ads
    # queryset = Ads.objects.all()
    template_name = 'ads_details.html'
    context_object_name = 'ads_details'


# PermissionRequiredMixin,
class AdsCreate(CreateView):
    form_class = AdsForm
    model = Ads
    # permission_required = ('News.add_post',)
    template_name = 'ads_edit.html'
    context_object_name = 'ads'


class AdsDelete(DeleteView):
    model = Ads
    # permission_required = ('News.delete_post',)
    template_name = 'ads_delete.html'
    success_url = reverse_lazy('ads_list')
