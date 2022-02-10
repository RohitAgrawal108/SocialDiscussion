from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Complaint
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
# from userpreferences.models import UserPreference
import datetime
from django.utils.timezone import now
#states
import os
import json
from django import forms
from django.conf import settings
#################################

# class TextArea(forms.Form):

#     body = forms.CharField(widget=forms.Textarea())


@login_required(login_url='/Authentication/login')
def index(request):
    categories = Category.objects.all().order_by('id')
    complaints = Complaint.objects.filter(owner=request.user)
    paginator = Paginator(complaints, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # try:
    #     currency = UserPreference.objects.get(user=request.user).currency
    #     context = {
    #     'expenses': expenses,
    #     'page_obj': page_obj,
    #     'currency': currency
    # }
    # user = None
    context = {
    'complaints': complaints,
    'page_obj': page_obj,
    }
    return render(request, 'Complaints/index.html', context)


@login_required(login_url='/Authentication/login')
def add_complaint(request):
    categories = Category.objects.all().order_by('id')
    
#####################################################################################
    state_data = []
    file_path = os.path.join(settings.BASE_DIR, 'states.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            state_data.append({'name': k, 'value': v})

    # exists = UserPreference.objects.filter(user=request.user).exists()
    # user_preferences = None
    # if exists:
    #     user_preferences = UserPreference.objects.get(user=request.user)
    # if request.method == 'GET':

    #     return render(request, 'preferences/index.html', {'currencies': currency_data,'user_preferences': user_preferences})

    context = {
        'categories': categories,
        'values': request.POST,
        'states': state_data,
        # 'textarea': TextArea()
    }
    

    if request.method == 'GET':
        return render(request, 'Complaints/add_complaint.html', context)

    if request.method == 'POST':
        
        # count = 1#request.POST['amount']
        count = 1
        against = request.POST['against']
        # complaint_date = now
        if not count:
            messages.error(request, 'Count is required')
            return render(request, 'Complaints/add_complaint.html', context)
        description = request.POST['description']
        date = request.POST['complaint_date']
        category = request.POST['category']
        state= request.POST['state']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'Complaints/add_complaint.html', context)

        Complaint.objects.create(owner=request.user, count=count, date=date,
                               category=category, description=description, against=against,state=state)
        messages.success(request, 'Complaint saved successfully')

        return redirect('Complaints')


@login_required(login_url='/Authentication/login')
def complaint_edit(request, id):
    complaint = Complaint.objects.get(pk=id)
    categories = Category.objects.all().order_by('id')
    context = {
        'complaint': complaint,
        'values': complaint,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'Complaints/edit-complaint.html', context)
    if request.method == 'POST':
        count = 1 #request.POST['amount']

        
        description = request.POST['description']
        date = request.POST['complaint_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'Complaints/edit-complaint.html', context)

        complaint.owner = request.user
        complaint.count = count
        complaint.date = date
        complaint.category = category
        complaint.description = description

        complaint.save()
        messages.success(request, 'Complaint updated  successfully')

        return redirect('Complaints')


def delete_complaint(request, id):
    complaint = Complaint.objects.get(pk=id)
    complaint.delete()
    messages.success(request, 'Complaint removed')
    return redirect('Complaints')


# def complaint_category_summary(request):
#     todays_date = datetime.date.today()
#     six_months_ago = todays_date-datetime.timedelta(days=30*6)
#     complaints = Complaint.objects.filter(owner=request.user,date__gte=six_months_ago, date__lte=todays_date)
#     finalrep = {}

#     def get_category(complaint):
#         return complaint.category
#     category_list = list(set(map(get_category, complaints)))

#     def get_complaint_category_count(category):
#         count = 0
#         filtered_by_category = complaints.filter(category=category)

#         for item in filtered_by_category:
#             count += item.count
#         return count

#     for x in complaints:
#         for y in category_list:
#             finalrep[y] = get_complaint_category_count(y)

#     return JsonResponse({'complaint_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'Complaints/stats.html')


# dashboard try
def dashboard_complaint_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    complaints = Complaint.objects.filter(date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(complaint):
        return complaint.category
    category_list = list(set(map(get_category, complaints)))

    def get_complaint_category_count(category):
        count = 0
        filtered_by_category = complaints.filter(category=category)

        for item in filtered_by_category:
            count += item.count
        return count

    for x in complaints:
        for y in category_list:
            finalrep[y] = get_complaint_category_count(y)

    return JsonResponse({'complaint_category_data': finalrep}, safe=False)

def complaint_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    complaints = Complaint.objects.filter(owner=request.user,date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(complaint):
        return complaint.category
    category_list = list(set(map(get_category, complaints)))

    def get_complaint_category_count(category):
        count = 0
        filtered_by_category = complaints.filter(category=category)

        for item in filtered_by_category:
            count += item.count
        return count

    for x in complaints:
        for y in category_list:
            finalrep[y] = get_complaint_category_count(y)

    return JsonResponse({'complaint_category_data': finalrep}, safe=False)

def dashboard_view(request):
    categories = Category.objects.all().order_by('id')
    complaints = Complaint.objects.all().order_by('id')
    paginator = Paginator(complaints, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
    'complaints': complaints,
    'page_obj': page_obj,
    }
    return render(request, 'Complaints/dashboard.html', context)

# def listdashboard_view(request):
#     return render(request, 'expenses/listdashboard.html')

def listdashboard_view(request):
    categories = Category.objects.all().order_by('id')
    complaints = Complaint.objects.all().order_by('id')
    paginator = Paginator(complaints, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # try:
    #     currency = UserPreference.objects.get(user=request.user).currency
    #     context = {
    #     'expenses': expenses,
    #     'page_obj': page_obj,
    #     'currency': currency
    # }
    # except UserPreference.DoesNotExist:
    #     user = None
    context = {
    'complaints': complaints,
    'page_obj': page_obj,
    }
    return render(request, 'Complaints/listdashboard.html', context)

def search_complaints(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        complaints = Complaint.objects.filter(
            count__istartswith=search_str, owner=request.user) | Complaint.objects.filter(
            date__istartswith=search_str, owner=request.user) | Complaint.objects.filter(
            description__icontains=search_str, owner=request.user) | Complaint.objects.filter(
            category__icontains=search_str, owner=request.user) | Complaint.objects.filter(
            against__icontains=search_str, owner=request.user)
        data = complaints.values()
        return JsonResponse(list(data), safe=False)


def dashboard_search_complaints(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        complaints = Complaint.objects.filter(
            count__istartswith=search_str) | Complaint.objects.filter(
            date__istartswith=search_str) | Complaint.objects.filter(
            description__icontains=search_str) | Complaint.objects.filter(
            category__icontains=search_str) | Complaint.objects.filter(
            against__icontains=search_str)
        data = complaints.values()
        return JsonResponse(list(data), safe=False)