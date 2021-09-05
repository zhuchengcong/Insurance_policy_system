import os
import re

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base_django_api.settings")
django.setup()

from user.models import Auth, AuthPermission

# 权限 初始化代码
# 主要生成 所有查看权限
# 生成 所有查看，所有新建权限
# 生成 所有查看，所有新建，所有编辑权限

from insurance.models import ChannelEffectiveTime, FeeField, InsurancePolicy

# q = FeeField.objects

# InsurancePolicy.objects.filter(chanel_rate_id__chanel=)
# ChannelEffectiveTime.objects.filter(chanel_id=)

from base_django_api.urls import router

url = {}

for i in router.urls:
    # print(type(i))
    # print(i)
    print(i.pattern.__dict__['_regex'])
    result = re.search(r'[a-zA-Z]{2,}', i.pattern.__dict__['_regex'])
    # print(result.group())
    if result is not None:
        url[result.group()] = result.group()

print('---------------------------------------------------------------------------------------------------------')
for key, values in url.items():
    print(key)

print('----------------------------------------------所有查看权限--------------------------------------------------')
auth = Auth.objects.create(auth_type="所有查看权限")

for key, values in url.items():
    AuthPermission.objects.create(auth=auth, object_name=key, object_name_cn=key, auth_list=True)

print('----------------------------------------------所有查看，新增权限--------------------------------------------------')
auth = Auth.objects.create(auth_type="查看,新增权限")

for key, values in url.items():
    AuthPermission.objects.create(auth=auth, object_name=key, object_name_cn=key, auth_list=True, auth_create=True)

print('----------------------------------------------所有查看,新增,编辑权限--------------------------------------------------')
auth2 = Auth.objects.create(auth_type="查看,新增,编辑权限")

for key, values in url.items():
    AuthPermission.objects.create(auth=auth2, object_name=key, object_name_cn=key, auth_list=True, auth_create=True)
