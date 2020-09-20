from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *
import random
from django.contrib import messages, auth
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about_us.html')

def view_login(request):  # always use different name than just 'login' because as u have imported login from django.contrib.auth, it is overriding login
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_obj = authenticate(request, username=username, password=password)  # authentic verified whether given username and password matches the existing user in database
        # print(user_obj)
        if user_obj != None:
            request.session.set_expiry(500)  # expiry time for session after inactivity  # given seconds value
            login(request, user_obj)  # user get logged in django
            messages.success(request, "Welcome... Login Successfully.")
            return HttpResponseRedirect(reverse('select_acc'))
        else:
            messages.warning(request, f"Sorry Is Invalid Username Or Password..!")
            return redirect('login')
    else:
        return render(request, 'login.html', )

def Create_new_acc(request):
    acc_no = random.randint(11111,99999)
    if request.method == "POST":
        data = request.POST
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user_obj = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname,email=email)
        cust_age = data.get('cust_age')
        cust_add =data.get('cust_add')
        cust_acc_type = data.get('cust_acc_type')
        # print(cust_acc_type)
        cust_balance = data.get('cust_balance')
        obj = Bank_Detail(cust_name=firstname, cust_age=cust_age, cust_add=cust_add, cust_balance=cust_balance, cust_acc_type=cust_acc_type, cust_acc_no=acc_no,user=user_obj)
        obj.save()
        messages.success(request, f"Account Created With {acc_no} Account Number.")
        return redirect('Create_new_acc')
    return render(request, 'Create_new_acc.html')

def another_acc(request):
    user = request.user
    user_id = request.user.id
    cust_name= user.first_name
    bank_obj = Bank_Detail.activeall.filter(user__id=user_id)
    for b in bank_obj:
        add =b
    cust_add=add.cust_add
    acc_no = random.randint(11111, 99999)
    try:
        if request.method == "POST":
            data = request.POST
            cust_acc_type = data.get('cust_acc_type')
            cust_balance = data.get('cust_balance')
            cust_age = data.get('cust_age')
            another_acc = Bank_Detail(cust_name=cust_name ,cust_acc_no=acc_no, cust_acc_type=cust_acc_type, cust_age=cust_age, cust_add=cust_add, cust_balance=cust_balance, user=user)
            another_acc.save()
            messages.success(request, f"Account Created With {acc_no} Account Number.")
            return redirect('select_acc')
        return render(request, 'another_acc.html')
    except:
        messages.warning(request, "Session Expired")
        return redirect('login')

def select_acc(request):
    user = request.user
    user_id = request.user.id
    try:
        bank_obj = Bank_Detail.activeall.filter(user__id=user_id)
        return render(request, 'select_acc.html', {'bank_obj':bank_obj, "u":user})
    except:
        messages.warning(request, "Session Expired")
        return redirect('login')

def detail(request, cust_acc_no):
    user = request.user
    try:
        bank_obj1 = Bank_Detail.activeall.get(cust_acc_no=int(cust_acc_no))
        request.session['acc_no'] = cust_acc_no
        if bank_obj1 != None:
            return render(request, 'detail.html', {"u": user, 'bank_obj1': bank_obj1})
        else:
            return render(request, 'select_acc.html')
    except:
        messages.warning(request, "Session Expired")
        return redirect('login')


def cust_add(request):
    user = request.user
    user_id = request.user.id
    bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
    bank_obj1 = Bank_Detail.activeall.filter(user__id=user_id)
    # print(bank_obj1)
    if request.method == "POST":
        cust_add =request.POST['cust_add']
        # print(cust_add)
        for b in bank_obj1:
            b.dummy_add = cust_add
            b.save()
    return render(request, 'cust_add.html', {'u': user, 'b1': bank_obj})

def status(request):
    user = request.user
    user_id = request.user.id
    try:
        bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
        if bank_obj.dummy_add == "":
            messages.success(request, "Request Approved")
        elif bank_obj.dummy_add == " ":
            messages.warning(request, "Request Rejected")
        else:
            messages.warning(request, "Request Pending")
        return render(request, 'cust_add.html', {'u': user, 'b1': bank_obj})
    except:
        messages.warning(request, "Session Expired")
        return redirect('login')


def deposit(request):
        user_id = request.user.id
        try:
            bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
            if request.method == "POST":
                dep_amt = int(request.POST['damount'])
                bank_obj.cust_balance += dep_amt
                bank_obj.save()
                messages.success(request, f"{dep_amt} Rs. Successfully Credited")
                #  Mail Send # ----------------------------
                # send_mail(f'Money Credited To {bank_obj.cust_acc_no} ', f'Hi {bank_obj.cust_name} {dep_amt}. Rs Credited Successfully', 'ameyshende30@gmail.com', ['ameyshende30@gmail.com'] )
                return redirect('detail', cust_acc_no= request.session['acc_no'])
            else:
                return render(request, 'deposit.html', {'b': bank_obj})
        except:
            messages.warning(request, "Session Expired")
            return redirect('login')

def withdraw(request):
    user_id = request.user.id
    try:
        bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
        if request.method == "POST":
            wit_amt = int(request.POST['wamount'])
            # print(wit_amt)
            if bank_obj.cust_balance > wit_amt :
                bank_obj.cust_balance -= wit_amt
                bank_obj.save()
                messages.success(request, f"{wit_amt} Rs. Successfully Debited.")
                return redirect('detail', cust_acc_no= request.session['acc_no'])
            else:
                messages.warning(request, "Insufficient Fuds !!! , Transition Failed")
                return redirect('withdraw')
        else:
            return render(request, 'withdraw.html', {'b': bank_obj})
    except:
        messages.warning(request, "Session Expired")
        return redirect('login')

def lone(request):
    user_id = request.user.id
    try:
        bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
        if request.method == "POST":
            lone_amt = int(request.POST['lamount'])
            lone_time = int(request.POST['ltime'])
            # print(lone_amt, lone_time)

            temp_bal = bank_obj.cust_balance - 1000
            if lone_amt <= temp_bal:
                INTEREST_RATE = 9.5
                int_amt = lone_amt * INTEREST_RATE / 100
                total_amt = int_amt + lone_amt
                monthely_paid = total_amt // lone_time
                bank_obj.cust_lone = lone_amt
                bank_obj.save()
                messages.success(request, f"Your's Lone Case Is Approved, You Have to Pay {monthely_paid} For {lone_time} Months Only. ")
                return redirect('detail', cust_acc_no= request.session['acc_no'])
            else:
                messages.warning(request,"Sorry Your's Lone Amount Is Too Hight As Compair To You's Current Balance ")
                return redirect('lone')
        else:
            if bank_obj.cust_balance < 30000 :
                messages.warning(request, "Insufficient Fuds !!! , Your Account Balnace Must Be Greater Than 30,000 ")
                return redirect('detail', cust_acc_no=request.session['acc_no'])
            return render(request, 'lone.html', {'b': bank_obj})
    except:
        messages.warning(request, "Session Expired")
        return redirect('login')

def Fd(request):
    user_id = request.user.id
    try:
        bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
        if request.method == "POST":
            FD_amt = int(request.POST['FDamt'])
            FD_time = int(request.POST['FDtime'])
            # print(FD_amt,FD_time)
            if FD_amt >= 20000:
                if FD_time >= 1:
                    FD_RATE = 6.5
                    Intrest_Amt = FD_amt * FD_RATE / 100
                    FD_profit = Intrest_Amt * FD_time
                    total_amt = FD_amt + FD_profit
                    bank_obj.cust_FD = FD_amt
                    bank_obj.save()
                    messages.success(request, f" FD Get Matured In {FD_time} Year And Total Benefits Is {total_amt}")
                    return redirect('detail', cust_acc_no=request.session['acc_no'])

                else:
                    messages.warning(request, "FD Time Period Must Be Greater Than 1 Year  ")
                    return redirect('Fd')
            else:
                messages.warning(request, "FD Amount Must Be Greater Than 20K. ")
                return redirect('Fd')

        return render(request, 'Fd.html', {'b': bank_obj})
    except:
        messages.warning(request, "Session Expired")
        return redirect('login')

def view_logout(request):
    # print(request.method, '###')
    if request.method == 'POST':
        logout(request)
        messages.success(request, "logout Successfully ")
        return redirect('login')


def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # print(username, password)
        user_obj = authenticate(request, username=username, password=password)
        # print(user_obj, "----------")
        if user_obj != None:
            if user_obj.username == "amey":
                request.session.set_expiry(500)
                login(request, user_obj)
                messages.success(request, "Welcome... LogIn Successfully.")
                return HttpResponseRedirect(reverse('admin_details'))
            else:
                messages.warning(request, f"Invalid Username Or Password. ", )
                return redirect('home')
        else:
            messages.warning(request, f"Invalid Username Or Password.", )
            return redirect('home')
    return render(request, 'admin_login.html')

def admin_details(request):
    bank_obj = Bank_Detail.activeall.all()
    inactive_acc = Bank_Detail.inactiveall.all()
    # print(bank_obj)
    # print(inactive_acc)
    return render(request, 'admin_details.html', {"bank_obj" : bank_obj, "inactive_acc" :inactive_acc})

def hard_delete(request, cust_acc_no):
    bank = Bank_Detail.activeall.get(cust_acc_no=cust_acc_no)
    bank.delete()
    return redirect(admin_details)

def soft_delete(request, cust_acc_no):
    bank_obj = Bank_Detail.activeall.get(cust_acc_no=cust_acc_no)
    status = bank_obj.active
    # print(status)
    if status == "Y":
        bank_obj.active = "N"
        bank_obj.save()
        return redirect(admin_details)
    return redirect(admin_details)

def recover_acc(request, cust_acc_no):
    bank_obj = Bank_Detail.inactiveall.get(cust_acc_no=cust_acc_no)
    status = bank_obj.active
    if status == "N":
        bank_obj.active = "Y"
        bank_obj.save()
        return redirect(admin_details)
    return redirect(admin_details)


def approve(request, cust_acc_no):
    bank_obj = Bank_Detail.activeall.get(cust_acc_no=cust_acc_no)
    #print(bank_obj.dummy_add)
    add =bank_obj.dummy_add
    if add != "":
        bank_obj.cust_add = add
        bank_obj.save()
        bank_obj.dummy_add = ""
        bank_obj.save()
    else:
        messages.warning(request, f"No Change Address request", )
    return redirect(admin_details)

def reject(request, cust_acc_no):
    bank_obj = Bank_Detail.activeall.get(cust_acc_no=cust_acc_no)
    add = bank_obj.dummy_add
    if add != "":
        bank_obj.dummy_add = " "
        bank_obj.save()
    else:
        messages.warning(request, f"No Change Address request", )
    return redirect(admin_details)


def send_money(request):
    user_id = request.user.id
    try:
        bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
        if request.method == "POST":
            sender_acc_no = int(request.POST['sender_acc_no'])
            send_amt = int(request.POST['send_amt'])
            if bank_obj.cust_balance > send_amt:
                if send_amt <= 10000:
                    bank_obj1 = Bank_Detail.activeall.get(cust_acc_no=sender_acc_no)
                    bank_obj1.cust_balance += send_amt
                    bank_obj.cust_balance -= send_amt
                    bank_obj1.save()
                    bank_obj.save()
                    messages.success(request, f"{send_amt} Rs. Successfully Send To {sender_acc_no} Acc No.")
                else:
                    messages.warning(request, "Amount Must Be Less Than 10K ")
                    return redirect('send_money')
            else:
                messages.warning(request, "Insufficient Fuds !!! , Transition Failed")
                return redirect('send_money')

        return render(request, 'send_money.html',{'b':bank_obj,})
    except:
        messages.warning(request, "Session Expired")
        return redirect('login')


def money_req_approve(request, req_money_accNo):
    user_id = request.user.id
    bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])  # login Obj
    req_money = int(bank_obj.req_money)
    if req_money != 0:
        if bank_obj.cust_balance > req_money:
            req_obj = Bank_Detail.activeall.get(cust_acc_no=req_money_accNo)
            # print(req_obj)
            name = req_obj.cust_name
            req_obj.cust_balance += req_money
            bank_obj.cust_balance -= req_money
            bank_obj.req_money = 0
            bank_obj.req_money_accNo = 0
            bank_obj.req_money_name = "No Current Request"
            req_obj.req_money_name = "No Current Request"
            bank_obj.save()
            req_obj.save()
            messages.success(request, f"{req_money} Rs. Debited Successfully, And Credited To {name}'s Account.")
            return redirect(send_money)
        else:
            messages.warning(request, "Insufficient Fuds !!! , Transition Failed")
            return redirect(send_money)
    else:
        messages.warning(request, "Current No Request Found..!! ")
        return redirect(send_money)


def money_req_reject(request, req_money_accNo):
    user_id = request.user.id
    bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
    req_money = int(bank_obj.req_money)
    if req_money != 0:
        req_obj = Bank_Detail.activeall.get(cust_acc_no=req_money_accNo)
        bank_obj.req_money = 0
        bank_obj.req_money_accNo = 0
        bank_obj.req_money_name = "No Current Request."
        req_obj.req_money_name = "No Current Request."
        bank_obj.save()
        req_obj.save()
        messages.warning(request, "Request Rejected..!!! ")
        return redirect(send_money)
    else:
        messages.warning(request, "Current No Request Found..!! ")
        return redirect(send_money)

def money_status(request):
    user_id = request.user.id
    try:
        bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
        # print(bank_obj.cust_acc_no, "---------------")
        if bank_obj.req_money_name == 'No Current Request.' and bank_obj.req_money == 0:
            messages.warning(request, "Request Rejected")
            return redirect(req_money)
        elif bank_obj.req_money_name == 'No Current Request' and bank_obj.req_money == 0:
            messages.success(request, "Request Approved")
            return redirect(req_money)
        elif bank_obj.req_money == 0:
            messages.warning(request, "Request Pending")
            return redirect(req_money)
    except:
        messages.warning(request, "Session Expired")
        return redirect('login')


def req_money(request):
    user_id = request.user.id
    bank_obj = Bank_Detail.activeall.get(user__id=user_id, cust_acc_no=request.session['acc_no'])
    if request.method == "POST":
        acc_no = int(request.POST['raccNo'])
        amt = int(request.POST['ramt'])
        if amt < 10000:
            bank_obj1 = Bank_Detail.activeall.get(cust_acc_no=acc_no)
            req_name = bank_obj.cust_name
            req_acc_no =bank_obj.cust_acc_no
            bank_obj1.req_money = amt
            bank_obj1.req_money_name = req_name
            bank_obj1.req_money_accNo = req_acc_no
            bank_obj1.save()
            messages.success(request, f"{amt} Rs. Request To {bank_obj1}")
            return redirect(req_money)
        else:
            messages.warning(request, "Request Amount Must Not Greater Than 10K ")
            return redirect(req_money)
    return render(request, 'req_money.html',{'b': bank_obj})

