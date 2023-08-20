from django.urls import path
# from django.views.decorators.cache import cache_page
from .views import (
    AdsList,
    AdsDetail,
    AdsCreate,
    AdsUpdate,
    AdsDelete,
    VerifyEmail,
    ReplyUpdate,
    ReplyDelete,
)


urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
    path('verify/', VerifyEmail.as_view(), name='verify_email'),
    path('create/', AdsCreate.as_view(), name='ads_create'),
    path('<int:pk>', AdsDetail.as_view(), name='ads_detail'),
    path('<int:pk>/edit', AdsUpdate.as_view(), name='ads_update'),
    path('<int:pk>/delete/', AdsDelete.as_view(), name='ads_delete'),
    path('reply/<int:pk>/edit', ReplyUpdate.as_view(), name='reply_update'),
    path('reply/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
]

# path('search/', AdsSearch.as_view(), name='ads_search'),
