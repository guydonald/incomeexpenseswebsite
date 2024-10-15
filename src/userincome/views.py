import json

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Source, UserIcome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.


def search_incomes(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        income = (
            UserIcome.objects.filter(amount__istartswith=search_str, owner=request.user)
            | UserIcome.objects.filter(date__istartswith=search_str, owner=request.user)
            | UserIcome.objects.filter(
                description__icontains=search_str, owner=request.user
            )
            | UserIcome.objects.filter(source__icontains=search_str, owner=request.user)
        )

        data = income.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url="/authentication/login")
def index(request):
    categories = Source.objects.all()
    income = UserIcome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        "income": income,
        "page_obj": page_obj,
        "currency": currency,
    }
    return render(request, "income/index.html", context)


@login_required(login_url="/authentication/login")
def add_income(request):
    sources = Source.objects.all()
    context = {"sources": sources, "values": request.POST}
    if request.method == "GET":
        return render(request, "income/add_income.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        date = request.POST["income_date"]
        description = request.POST["description"]
        source = request.POST["source"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "income/add_income.html", context)

        if not description:
            messages.error(request, "description is required")
            return render(request, "income/add_income.html", context)

        UserIcome.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            source=source,
            description=description,
        )
        messages.success(request, "Record saved successfully")
        return redirect("income")

@login_required(login_url="/authentication/login")
def income_edit(request, id):
    income = UserIcome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {"income": income, "value": income, "sources": sources}
    if request.method == "GET":

        return render(request, "income/edit_income.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        date = request.POST["income_date"]
        description = request.POST["description"]
        source = request.POST["source"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "income/edit_income.html", context)

        if not description:
            messages.error(request, "description is required")
            return render(request, "income/edit_income.html", context)

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.save()
        messages.success(request, "Record updated  successfully")
        return redirect("income")

def delete_income(request, id):
    income = UserIcome.objects.get(pk=id)
    income.delete()
    messages.success(request, "record removed")
    return redirect("income")