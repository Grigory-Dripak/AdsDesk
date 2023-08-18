from django.urls import path
# from django.views.decorators.cache import cache_page
from .views import (AdsList, AdsDetail, AdsCreate, AdsDelete, VerifyEmail)
#                     ,
#                     PostsSearch,
#                     New,
#                     ArticleCreate,
#                     NewsUpdate,
#                     ArticleUpdate,
#                     NewsDelete,
#                     ArticleDelete
#                     )


urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
    path('<int:pk>', AdsDetail.as_view(), name='ads_detail'),
    path('create/', AdsCreate.as_view(), name='ads_create'),
    path('<int:pk>/delete/', AdsDelete.as_view(), name='ads_delete'),
    path('verify/', VerifyEmail.as_view(), name='verify_email'),
]

# path('search/', AdsSearch.as_view(), name='ads_search'),
