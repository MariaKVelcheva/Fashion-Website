from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your name"},
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email"},
        )
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Your message..."},
        )
    )

