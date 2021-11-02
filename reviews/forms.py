from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    # the choices for ChoiceField should be tuple of tuples or it can be list of lists
    search_choices = (("title", "Title"), ("contributor", "Contributor"))
    search_in = forms.ChoiceField(required=False, choices=search_choices)
