from django.shortcuts import render, redirect
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

    def post(self, request, *args, **kwargs):
        # form = AdsForm(request.POST)
        # if not self.request.user.groups.filter(name='virified_email').exists():
        #     form = ...Form()
        #     return redirect(to='verify_email')
        ads = Ads(
            category=request.POST['category'],
            title=request.POST['title'],
            # seller=self.request.user,
            content=request.POST['content']
        )
        ads.save()
        return redirect(to='ads_list')


class AdsDelete(DeleteView):
    model = Ads
    # permission_required = ('News.delete_post',)
    template_name = 'ads_delete.html'
    success_url = reverse_lazy('ads_list')
