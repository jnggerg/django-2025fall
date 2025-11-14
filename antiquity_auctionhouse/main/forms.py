from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['worker', 'rating', 'comment']
        labels = {
            'worker': 'Munkatárs',
            'rating': 'Értékelés (1-5)',
            'comment': 'Megjegyzés'
        }
        help_texts = {
            'rating': 'Adjon 1-től 5-ig terjedő értékelést',
            'comment': 'Maximum 500 karakter'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Írja le véleményét...'})
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (1 <= rating <= 5):
            raise forms.ValidationError('Az értékelés 1 és 5 közé eső érték kell hogy legyen.')
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if comment and len(comment) > 500:
            raise forms.ValidationError('A megjegyzés maximum 500 karakter lehet.')
        return comment
    
    