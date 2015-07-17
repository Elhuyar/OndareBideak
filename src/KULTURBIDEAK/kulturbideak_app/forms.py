from django.forms import *
from django.core.validators import validate_email
from django.forms.extras.widgets import SelectDateWidget
import django.forms.extras
from django.db.models import Q
from django.contrib.auth.models import User
#Mad
from django import forms
from django.utils.translation import ugettext_lazy as _
#from django.utils.translation import ungettext_lazy

HIZKUNTZA_CHOICES = (
    (1, 'Euskera'),
    (2, 'Gaztelania'),
    (3, 'Ingelesa'),
)



class LoginForm(Form):
    """Earbiltzaile bat logeatzeko formularioa kargatzen du"""
    erabiltzailea=CharField(max_length=150,required=True, widget=TextInput(attrs={"placeholder":_("erabiltzailea"),"type":"text", "class":"form-control"}))
    pasahitza=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("pasahitza"),"type":"password", "class":"form-control"}),required=True)

    def clean_erabiltzailea(self):
        """Erabiltzailea existitzen den konprobatzen da"""
        try:
            e=User.objects.get(username=self.cleaned_data["erabiltzailea"])
            return self.cleaned_data["erabiltzailea"]
        except:
            raise forms.ValidationError("Erabiltazilea ez dago erregistratua")

    def clean_pasahitza(self):
        """Erabiltzailea eta pasahitza egokia diren konprobatzen da"""
        error_message =_("Pasahitza ez da zuzena")
        try:
            e=User.objects.get(username=self.cleaned_data["erabiltzailea"])
            if e.check_password(self.cleaned_data["pasahitza"]):
                return self.cleaned_data["pasahitza"]
            else:
                raise forms.ValidationError(error_message)
        except:
            raise forms.ValidationError(error_message)
        
        
class CreateUserForm(forms.Form):
    '''
    posta=forms.CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Helbide elektronikoa"),"type":"text", "class":"form-control","id":"InputEmail"}))
    password=forms.CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("Pasahitza"),"type":"password", "class":"form-control","id":"InputPass"}),required=True)
    password2=forms.CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("Errepikatu pasahitza"),"type":"password", "class":"form-control","id":"InputPass2"}),required=True)
    izena=forms.CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Izena"),"type":"text", "class":"form-control","id":"InputName"}))
    abizena=forms.CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Abizenak"),"type":"text", "class":"form-control","id":"InputName2"}))
    username=forms.CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Erabiltzailea"),"type":"text", "class":"form-control","id":"InputUser"}))
    erabiltzaile_mota = DynamicChoiceField(required=False)
     '''
    izena=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Izena"),"type":"text", "class":"form-control","id":"InputName"}))
    abizena=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Abizenak"),"type":"text", "class":"form-control","id":"InputName2"}))
    username=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Erabiltzailea"),"type":"text", "class":"form-control","id":"InputUser"}))
    
    posta=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Helbide elektronikoa"),"type":"text", "class":"form-control","id":"InputEmail"}))
    password=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("Pasahitza"),"type":"password", "class":"form-control","id":"InputPass"}),required=True)
    password2=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("Errepikatu pasahitza"),"type":"password", "class":"form-control","id":"InputPass2"}),required=True)
   
    ##erabiltzaile_mota = DynamicChoiceField(required=False)
    
    
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
       # self.fields['posta'].help_text="Pasahitza helbide honetara bidaliko zaio"
        """if user.has_advanced_admin_permissions():
            erabiltzaile_mota_choices = [("standard_user","Erabiltzaile arrunta"),("advanced_user","Erabiltzaile aurreratua"),("standard_admin","Administratzaile arrunta"),("advanced_admin","Administratzaile aurreratua")]
        else: #standard admin"""
        ##erabiltzaile_mota_choices = [("superadministratzailea","SuperAdministratzailea"),("kudeatzailea","Kudeatzailea"),("bideratzailea","Bideratzailea"),("editorea","Editorea")]
        ##self.fields['erabiltzaile_mota'].choices = erabiltzaile_mota_choices        

    def clean_username(self):
        cleaned_data = self.cleaned_data
        error_message=_("Erabiltzaile izen hau dagoeneko erregistratua dago")
        if User.objects.filter(username=cleaned_data['username']).count() > 0:
            raise forms.ValidationError(error_message)
        else:
            return cleaned_data['username']

    def clean(self):
        error_message=_("Pasahitzak ezberdinak dira")
        try:
                cleaned_data = self.cleaned_data
                if cleaned_data['password']!=cleaned_data['password2']:
                    self._errors['password2'] = self.error_class([error_message])
                else:
                    return cleaned_data
        except:
                pass

class UserProfileForm(forms.Form):
    '''
    posta=forms.CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Helbide elektronikoa"),"type":"text", "class":"form-control","id":"InputEmail"}))
    password=forms.CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("Pasahitza"),"type":"password", "class":"form-control","id":"InputPass"}),required=True)
    password2=forms.CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("Errepikatu pasahitza"),"type":"password", "class":"form-control","id":"InputPass2"}),required=True)
    izena=forms.CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Izena"),"type":"text", "class":"form-control","id":"InputName"}))
    abizena=forms.CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Abizenak"),"type":"text", "class":"form-control","id":"InputName2"}))
    username=forms.CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Erabiltzailea"),"type":"text", "class":"form-control","id":"InputUser"}))
    erabiltzaile_mota = DynamicChoiceField(required=False)
     '''
    izena=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Izena"),"type":"text", "class":"form-control","id":"InputName"}))
    abizena=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Abizenak"),"type":"text", "class":"form-control","id":"InputName2"}))
    username=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Erabiltzailea"),"type":"text", "class":"form-control","id":"InputUser"}))
    
    posta=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Helbide elektronikoa"),"type":"text", "class":"form-control","id":"InputEmail"}))
    '''
    PasahitzZaharra=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":"Pasahitz zaharra","type":"password", "class":"form-control","id":"InputPass"}),required=True)
    password=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":"Pasahitz berria","type":"password", "class":"form-control","id":"InputPass2"}),required=True)
    password2=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":"Errepikatu pasahitza","type":"password", "class":"form-control","id":"InputPass2"}),required=True)
    '''
   
    ##erabiltzaile_mota = DynamicChoiceField(required=False)
    
    
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # self.fields['posta'].help_text="Pasahitza helbide honetara bidaliko zaio"
        """if user.has_advanced_admin_permissions():
            erabiltzaile_mota_choices = [("standard_user","Erabiltzaile arrunta"),("advanced_user","Erabiltzaile aurreratua"),("standard_admin","Administratzaile arrunta"),("advanced_admin","Administratzaile aurreratua")]
        else: #standard admin"""
        ##erabiltzaile_mota_choices = [("superadministratzailea","SuperAdministratzailea"),("kudeatzailea","Kudeatzailea"),("bideratzailea","Bideratzailea"),("editorea","Editorea")]
        ##self.fields['erabiltzaile_mota'].choices = erabiltzaile_mota_choices        

    def clean_username(self):
        cleaned_data = self.cleaned_data
        
        return cleaned_data['username']
        '''
        if User.objects.filter(username=cleaned_data['username']).count() > 0:
            raise forms.ValidationError("Erabiltzaile izen hau dagoeneko erregistratua dago")
        else:
            return cleaned_data['username']
        '''

class ChangePasswordForm(forms.Form):
    """Erabiltzaileak pasahitza aldatzeko formularioa kargatzen du"""
    password=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("Pasahitz berria"),"type":"password", "class":"form-control","id":"InputPass2"}),required=True)
    password2=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("Errepikatu pasahitza"),"type":"password", "class":"form-control","id":"InputPass2"}),required=True)
    
    
    def clean(self):
        
        error_message=_("Pasahitzak ezberdinak dira")
        try:
                cleaned_data = self.cleaned_data
                if cleaned_data['password']!=cleaned_data['password2']:
                    self._errors['password2'] = self.error_class([error_message])
                else:
                    return cleaned_data
        except:
                pass
    
    
#    https://docs.djangoproject.com/en/1.8/ref/forms/fields/#multiplechoicefield   
class ItemGehituForm(Form):
    """Item berri bat gehitzeko formularioa kargatzen du"""
    titulua=CharField(max_length=500,required=True, widget=TextInput(attrs={"placeholder":_("titulua"),"type":"text", "class":"form-control"}))
    #  sortzailea: logeatuta dagoen erabiltzailea
    deskribapena=CharField(max_length=150,required=True, widget=TextInput(attrs={"placeholder":_("deskribapena"),"type":"text", "class":"form-control"}))
    # date : momentukoa
    gaia=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("gaia"),"type":"text", "class":"form-control"}))
    eskubideak=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("eskubideak"),"type":"text", "class":"form-control"}))
    irudia=ImageField(max_length=32,required=False)
    hizkuntza=ChoiceField(required=False,  choices=HIZKUNTZA_CHOICES)
    
class ItemEditatuForm(Form):
    """Item bat editatzeko formularioa kargatzen du"""
    titulua=CharField(max_length=500,required=True, widget=TextInput(attrs={"placeholder":_("titulua"),"type":"text", "class":"form-control"}))
    #  sortzailea: logeatuta dagoen erabiltzailea
    deskribapena=CharField(max_length=150,required=True, widget=TextInput(attrs={"placeholder":_("deskribapena"),"type":"text", "class":"form-control"}))
    # date : momentukoa
    gaia=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("gaia"),"type":"text", "class":"form-control"}))
    eskubideak=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("eskubideak"),"type":"text", "class":"form-control"}))
    irudia=ImageField(max_length=32,required=False)
    hizkuntza=ChoiceField(required=False,  choices=HIZKUNTZA_CHOICES)
    hidden_Item_id = CharField(label='reset',max_length=256, widget=forms.HiddenInput())