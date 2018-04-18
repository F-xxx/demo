from django.test import TestCase

# Create your tests here.
#
# def user_manage(request,uid=None,action=None):
#     if uid:
#         user = get_object_or_404(User_Profile,pk=uid)
#         if action == "delete":
#             user.delete()
#             Audit.objects.create(
#                 type='用户管理',
#                 user=request.user,
#                 action='删除',
#                 action_ip=login_ip(request),
#                 content='操作人：%s 被删除的用户 %s' % (request.user,user.email)
#             )
#             return redirect('user_list')
#     else:
#         # user = UserManager.create()
#         user = User_Profile()
#         action = 'add'
#
#     if request.method == 'POST':
#         form = UserModelForm(request.POST,instance=user)
#         if form.is_valid():
#             password1 = request.POST.get('password1')
#             password2 = request.POST.get('password2')
#             group_select = request.POST.get('group_sel')
#             group_delete = request.POST.get('group_del')
#             perm_select = request.POST.getlist('perm_sel')
#             perm_delete = request.POST.getlist('perm_del')
#             if action == 'add' or action == 'edit':
#                 form.save()
#                 if password1 and password1 == password2:
#                     user.set_password(password1)
#                 user.save()
#                 user.groups.add(*group_select)
#                 user.groups.remove(*group_delete)
#                 user.user_permissions.add(*perm_select)
#                 user.user_permissions.remove(*perm_delete)
#                 Audit.objects.create(
#                     type='用户管理',
#                     user=request.user,
#                     action='编辑',
#                     action_ip=login_ip(request),
#                     content='操作人：%s 编辑 %s' % (request.user, user.email)
#                 )
#                 return redirect('user_list')
#         else:
#             form = UserModelForm(instance=user)
#     return render(request,'userperm/user-manage.html',{'form':form,'uid':uid,'action':action})




















