from django import forms

SelectRole = (("BAT","BAT"),("WK","WK"), ("BOWL","BOWL"), ("ALL","ALL"))
class Player_List(forms.Form):
    Name = forms.CharField(max_length=264)
    Role = forms.ChoiceField(choices=SelectRole)
    Credit = forms.FloatField()
