from django.urls import path
from .import views

urlpatterns = [

    path('', views.index, name='home'),
    path('about_us', views.about_us, name='about_us'),
    path('login/', views.view_login, name='login'),
    path('Create_new_acc/', views.Create_new_acc, name='Create_new_acc'),
    path('detail/<int:cust_acc_no>/', views.detail, name='detail'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('lone/', views.lone, name='lone'),
    path('Fd/', views.Fd, name='Fd'),
    path('cust_add/', views.cust_add, name='cust_add'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_details/', views.admin_details, name='admin_details'),
    path('logout/', views.view_logout, name='logout'),
    path('select_acc/', views.select_acc, name='select_acc'),
    path('send_money/', views.send_money, name='send_money'),
    path('another_acc/', views.another_acc, name='another_acc'),
    path('hard_delete/<int:cust_acc_no>/',views.hard_delete, name='hard_delete'),
    path('soft_delete/<int:cust_acc_no>/',views.soft_delete, name='soft_delete'),
    path('recover_acc/<int:cust_acc_no>/',views.recover_acc, name='recover_acc'),
    path('approve/<int:cust_acc_no>/',views.approve, name='approve'),
    path('reject/<int:cust_acc_no>/',views.reject, name='reject'),
    path('money_req_approve/<int:req_money_accNo>/',views.money_req_approve, name='money_req_approve'),
    path('money_req_reject/<int:req_money_accNo>/',views.money_req_reject, name='money_req_reject'),
    path('status/',views.status, name='status'),
    path('money_status/',views.money_status, name='money_status'),
    path('req_money/',views.req_money, name='req_money'),

]

