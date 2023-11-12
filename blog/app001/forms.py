from django import forms
from .models import Post, Expense, Income
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    tags_str = forms.CharField(
        max_length=255,
        label='Tags (comma-separated)',
        required=False
    )

    image = forms.ImageField(
        label='Image',
        widget=forms.FileInput(attrs={'id': 'button', 'accept': 'image/*'}),
        required=False  # Make the field not required
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags_str', 'image']
        widgets = {
            'content': CKEditorWidget(config_name='default')
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount']  # Remove 'date' to let the model automatically set the date

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount']  # Remove 'date' to let the model automatically set the date
