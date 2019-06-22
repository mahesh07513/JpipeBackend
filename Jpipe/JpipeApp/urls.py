from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import *
from django.conf import settings


urlpatterns = [

    url(r'^JpipeUser/add_user/', csrf_exempt(add_user), name='add_user'),
    url(r'^JpipeUser/login/', csrf_exempt(login), name='login'),
    url(r'^JpipeUser/add_device/', csrf_exempt(add_device), name='add_device'),
    url(r'^JpipeUser/get_devices/', csrf_exempt(get_devices), name='get_devices'),
    url(r'^JpipeUser/add_snipet/', csrf_exempt(add_snipet), name='add_snipet'),
    url(r'^JpipeUser/get_snipets/', csrf_exempt(get_snipets), name='get_snipets'),
########################################
	url(r'^JpipeCompany/add_company/', csrf_exempt(add_company), name='add_company'),
    url(r'^JpipeCompany/update_company/', csrf_exempt(update_company), name='update_company'),
    url(r'^JpipeCompany/add_company_user/', csrf_exempt(add_company_user), name='add_company_user'),
    url(r'^JpipeCompany/get_jpipe_companies/', csrf_exempt(get_jpipe_companies), name='get_jpipe_companies'),
    url(r'^JpipeCompany/get_company_users/', csrf_exempt(get_company_users), name='get_company_users'),
    url(r'^JpipeCompany/add_dconfig_Type/', csrf_exempt(add_dconfig_Type), name='add_dconfig_Type'),
    url(r'^JpipeCompany/add_serial_Type/', csrf_exempt(add_serial_Type), name='add_serial_Type'),
    url(r'^JpipeCompany/add_dconfig_Operations/', csrf_exempt(add_dconfig_Operations), name='add_dconfig_Operations'),
    url(r'^JpipeCompany/add_dconfig_details/', csrf_exempt(add_dconfig_details), name='add_dconfig_details'),
    url(r'^JpipeCompany/get_dconfig_Type/', csrf_exempt(get_dconfig_Type), name='get_dconfig_Type'),
    url(r'^JpipeCompany/get_dconfig_Operations/', csrf_exempt(get_dconfig_Operations), name='get_dconfig_Operations'),
    url(r'^JpipeCompany/get_dconfig_details/', csrf_exempt(get_dconfig_details), name='get_dconfig_details'),
########################################
   url(r'^JpipeDevice/add_data/', csrf_exempt(add_data), name='add_data'),
   url(r'^JpipeDevice/add_device_config_mapping/', csrf_exempt(add_device_config_mapping), name='add_device_config_mapping'),
################### adapter ###############################
   url(r'^JpipeAdapter/add_adapter/', csrf_exempt(add_adapter), name='add_adapter'),
    









]