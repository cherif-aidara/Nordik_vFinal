from django import forms



from .models import Client, ClientInteraction





class ClientForm(forms.ModelForm):

    """Formulaire de création / édition de client.



    Les indicateurs (fidélité, satisfaction, nombre de commandes, montant

    dépensé) sont gérés automatiquement et ne sont pas saisis ici.

    """



    last_activity_date = forms.DateField(

        label="Dernière activité",

        required=False,

        widget=forms.DateInput(attrs={"type": "date"}),

    )



    class Meta:

        model = Client

        fields = [

            "name",

            "email",

            "phone",

            "address",

            "client_type",

            "status",

            "last_activity_date",

            "notes",

        ]

        widgets = {

            "address": forms.Textarea(attrs={"rows": 2}),

            "notes": forms.Textarea(attrs={"rows": 3}),

        }



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            css = field.widget.attrs.get("class", "")

            field.widget.attrs["class"] = (css + " pgi-input").strip()

            if not field.widget.attrs.get("placeholder"):

                field.widget.attrs["placeholder"] = field.label





class ClientInteractionForm(forms.ModelForm):

    """Formulaire de création d'une interaction client."""



    interaction_date = forms.DateTimeField(

        label="Date de l'interaction",

        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),

    )



    class Meta:

        model = ClientInteraction

        fields = [

            "client",

            "interaction_type",

            "subject",

            "description",

            "interaction_date",

            "user_name",

        ]

        widgets = {

            "description": forms.Textarea(attrs={"rows": 3}),

        }



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            css = field.widget.attrs.get("class", "")

            field.widget.attrs["class"] = (css + " pgi-input").strip()

            if not field.widget.attrs.get("placeholder"):

                field.widget.attrs["placeholder"] = field.label

