# If you're building a database-driven app, chances are you'll have forms that map closely to Django models. 
# In this case, it would be redundant to define the field types in your form, because you’ve already defined the fields in your model.
# For this reason, Django provides a nested class that lets you create a Form class from a Django model.
from django import forms
from .models import Listing, Bid, Comment, Category

class ListingForm(forms.ModelForm):
    # We are going to create a ModelForm subclass. A model form has to have a model to work from, 
    # and the Meta object configures this. Configuration like this is grouped into the "Meta" class to avoid name clashes; 
    # that way you can have a model field in your form without that interfering with the configuration. 
    # In other words, by using class Meta: you get a nested namespace used just to configure the ModelForm in relation to the model.
    class Meta:
        # Set the name of the model to be bound to the form.
        model = Listing

        # Use "fields" to specify which fields in the model should be displayed in the template.
        # If we want all fields in the model should be used in the template, We can set: fields = "__all__".
        fields = ["name", "description", "img", "starting_price", "category"]
        
        # Like in Django Forms, using "widgets" you can specify a dictionary of values to customize the ModelForm's widget class for a particular field.
        widgets = {
            "name": forms.TextInput(attrs={"autofocus":True, "placeholder":"Enter your listing name", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows":"4", "placeholder":"Describe your listing", "class":"form-control"}),
            "img": forms.URLInput(attrs={"placeholder":"Enter your listing URL", "class": "form-control"}),
            "starting_price": forms.NumberInput(attrs={"min":0, "placeholder":"Enter your starting price", "class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"})
        }

        # Use "labels" to change the titles of fields like in Django Forms.
        labels = {
            "img": "Image URL"
        }
    

    def __init__(self, *args, **kwargs):  # Note that this is not inside the "Meta" class.
        super(ListingForm, self).__init__(*args, **kwargs)

        # Sort the form's category field in alphabetical order.
        self.fields["category"].queryset = self.fields["category"].queryset.order_by("name")

        # Change the first option (which is default ) from "---------" the following sentence.
        self.fields["category"].empty_label = "Select category (leave it if no matching category)"

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields= ["listing", "amount"]
        widgets = {}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields= ["message"]
        widgets = {}