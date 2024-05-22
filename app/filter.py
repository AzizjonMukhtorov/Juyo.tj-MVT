



def expense_list(request):
    form = ExpenseFilterForm(request.GET)
    expenses = Expense.objects.all()

    if form.is_valid():
        if form.cleaned_data['expense_category']:
            expenses = expenses.filter(expense_category=form.cleaned_data['expense_category'])
        if form.cleaned_data['expense_payment_method']:
            expenses = expenses.filter(expense_payment_method=form.cleaned_data['expense_payment_method'])
        if form.cleaned_data['min_amount']:
            expenses = expenses.filter(expense_amount__gte=form.cleaned_data['min_amount'])
        if form.cleaned_data['max_amount']:
            expenses = expenses.filter(expense_amount__lte=form.cleaned_data['max_amount'])


    return render(request, 'expense_list.html', {'form': form, 'expenses': expenses})