from django import forms

class NewSearchEntryForm(forms.Form):
    searchEntry = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    pageTitle = forms.CharField(label="Title", widget=forms.TextInput(attrs={"class":"form-group"}))
    markdownContent = forms.CharField(label="MarkDown Content", widget=forms.Textarea(attrs={"class":"form-group"}), empty_value="hellowow")

class NewEditForm(forms.Form):

    markdownContent = forms.CharField(label="MarkDown Content", widget=forms.Textarea(attrs={"class":"form-group"}))