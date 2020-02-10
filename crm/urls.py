from django.conf.urls import url,include
from crm.views import consultant

urlpatterns = [
    # 展示公户列表
    url(r'customer_list/',consultant.CustomerList.as_view(),name='customer'),
    # 展示私户列表
    url(r'my_customer/',consultant.CustomerList.as_view(),name='my_customer'),
]