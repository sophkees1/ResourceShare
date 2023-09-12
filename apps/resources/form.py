from django import forms 


class PostResourceForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "title-input",
                "placeholder": "Enter a title"})) # input with type="text"
    
    link = forms.URLField(
        widget=forms.TextInput(
            attrs={"class": "link-input",
                "placeholder": "Enter a valid URL"}))
    
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "description-input"}))
    
    category = forms.ChoiceField(
        widget=forms.RadioSelect,
            choices=[
                ("3", "Programming Language"),
                ("2", "Databases"),
                ("5", "Frameworks"),
            ])
    
    tags = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=(
            ("10", "C++"),
            ("9", "PostgreSQL"),
            ("8", "SQL"),
            ("7", "Intermediate"),
            ("6", "Advanced"),
            ("5", "Beginner"),
            ("4", "Paid"),
            ("3", "Free"),
            ("2", "Django"),
            ("1", "Python"),
    ))
