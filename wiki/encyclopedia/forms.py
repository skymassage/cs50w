from django import forms

class EntryForm(forms.Form):
    # If we don't set the "label" attribute, the variable name will display as <label> and its first character also be capitalized.
    # "required=True" means the "required" attribute of <input>.
    # A "widget" is Django's representation of an HTML input element. The widget handles the rendering of the HTML, 
    # and the extraction of data from a GET/POST dictionary that corresponds to the widget.
    # Widgets should not be confused with the form fields. Form fields deal with the logic of input validation 
    # and are used directly in templates. Widgets deal with rendering of HTML form input elements on the web page 
    # and extraction of raw submitted data.
    # Whenever you specify a field on a form, Django will use a default widget that is appropriate to the type of data that is to be displayed.
    # The default of "widget" is "TextInput" (i.e. <input>). Choose "Textarea" (i.e. <textarea>) to use multi-line text field.
    # Use the "attrs" argument to specify the attributes of the field for CSS styling.
    title = forms.CharField(label="", required=True,  widget=forms.TextInput(attrs={
        "style":"height: 35px; width: 850px;", "class":"form-control", "id":"title_create"
    }))
    content = forms.CharField(label="", required=True, widget=forms.Textarea(attrs={
        "style":"height: 400px; width: 850px;", "class":"form-control", "id":"content_create"
    }))
