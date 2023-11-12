from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Expense, Income # Replace 'Post' with your actual model names, e.g., 'Expense' and 'Income'
from .forms import PostForm, ExpenseForm, IncomeForm  # Replace 'PostForm' with your actual form names
from django.db.models import Sum
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
import io
from reportlab.platypus import Paragraph
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from io import BytesIO
from django.shortcuts import HttpResponseRedirect
from reportlab.lib.units import inch
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
def calculate_totals(user):
    total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    return total_income, total_expenses
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()  # Save the post to the database

            # Now you can add tags
            post.set_tags(form.cleaned_data['tags_str'])

            return redirect('home_view')  # Replace 'post_list' with your view name for listing posts
    else:
        form = PostForm()
    return render(request, 'add_link.html', {'form': form})

def mon_view(request):
    income_items = Income.objects.all().order_by('-amount')
    expense_items = Expense.objects.all().order_by('-amount')

    try:
        total_income, total_expenses = calculate_totals(request.user)  # Calculate totals for the current user
    except TypeError:
        if isinstance(request.user, AnonymousUser):
            # Handle the case where the user is not authenticated
            return HttpResponse("User is not authenticated. Please log in.")
        else:
            # Handle other possible exceptions
            return HttpResponse("An error occurred while calculating totals.")

    remaining_amount = total_income - total_expenses
    debt_amount = total_expenses - total_income

    context = {
        'income_items': income_items,
        'expense_items': expense_items,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'remaining_amount': remaining_amount,
        'debt_amount': debt_amount,
    }

    return render(request, 'money.html', context)


def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Set the user to the currently logged-in user
            expense.save()
            return redirect('mon_view')
    else:
        form = ExpenseForm()
    return render(request, 'create_expense.html', {'form': form})

def create_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Set the user to the currently logged-in user
            income.save()
            return redirect('mon_view')
    else:
        form = IncomeForm()
    return render(request, 'create_income.html', {'form': form})

def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expense_list.html', {'expenses': expenses})

def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, 'income_list.html', {'incomes': incomes})
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    expense.delete()
    return redirect('mon_view')  # Redirect to the appropriate page after deletion.

def download_st(request):
    income_items = Income.objects.filter(user=request.user)
    expense_items = Expense.objects.filter(user=request.user)

    total_income = calculate_totals(request.user)[0]
    total_expenses = calculate_totals(request.user)[1]

    remaining_amount = total_income - total_expenses
    debt_amount = total_expenses - total_income

    # Create a buffer to hold the PDF content
    buffer = io.BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to hold the elements of the PDF
    elements = []

    # Define your preformatted headings and text
    preformatted_text = "This is your financial summary."

    # Create a table for income items
    income_data = [["Date", "Source", "Amount"]] + [[item.date, item.source, item.amount] for item in income_items]
    income_table = Table(income_data, colWidths=[1.5 * inch, 2 * inch, 1.5 * inch])  # Adjust the colWidths
    income_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Create a table for expense items
    expense_data = [["Date", "Description", "Amount"]] + [[item.date, item.description, item.amount] for item in expense_items]
    expense_table = Table(expense_data, colWidths=[1.5 * inch, 2.5 * inch, 1.5 * inch])  # Adjust the colWidths
    expense_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(Paragraph("Financial Summary", getSampleStyleSheet()["Title"]))
    elements.append(Paragraph(preformatted_text, getSampleStyleSheet()["Normal"]))
    elements.append(Paragraph("Income Items", getSampleStyleSheet()["Heading1"]))
    elements.append(income_table)
    elements.append(Paragraph("Expense Items", getSampleStyleSheet()["Heading1"]))
    elements.append(expense_table)

    # Build the PDF document
    doc.build(elements)

    # Reset the buffer position and create a FileResponse
    buffer.seek(0)
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="financial_summary.pdf"'
    return response