<<<<<<< HEAD
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'picture', 'description', 'price', 'deposit', 'interest_rate', 'acquired']

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        deposit = cleaned_data.get("deposit")
        if deposit > price:
            self.add_error('deposit', "Deposit cannot exceed the price.")
        elif deposit == price:
            cleaned_data['acquired'] = True
        return cleaned_data
=======
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'picture', 'description', 'price', 'deposit', 'interest_rate', 'acquired']

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        deposit = cleaned_data.get("deposit")
        if deposit > price:
            self.add_error('deposit', "Deposit cannot exceed the price.")
        elif deposit == price:
            cleaned_data['acquired'] = True
        return cleaned_data
>>>>>>> 56e8ba141c7ecebe8811d153cbf7b97be881f469
