from typing import ItemsView
from django import forms 
from inventory.models import Quest

class QuestForm(forms.ModelForm):
    class Meta:
        model=Quest
        fields = ['location', 'name', 'description', 'list_price', 'image']
