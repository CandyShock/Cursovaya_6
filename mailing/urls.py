from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import SettingListViews, SettingCreateView, SettingDetailView, SettingUpdateView, SettingDeleteView, \
    LogListView, LogDetailView, IndexView, SettingStatusMailing, ClientListView, ClientDetailView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index_list'),
    path('setting/', SettingListViews.as_view(), name='setting_list'),
    path('setting/create/', SettingCreateView.as_view(), name='setting_create'),
    path('setting/<int:pk>', SettingDetailView.as_view(), name='setting_detail'),
    path('setting/update/<int:pk>/', SettingUpdateView.as_view(), name='setting_update'),
    path('setting/delete/<int:pk>/', SettingDeleteView.as_view(), name='setting_delete'),
    path('log/', LogListView.as_view(), name='log_list'),
    path('log/<int:pk>/', LogDetailView.as_view(), name='log_details'),
    path('block-status/<int:pk>/', SettingStatusMailing.as_view(), name='setting_status'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client/create', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]

