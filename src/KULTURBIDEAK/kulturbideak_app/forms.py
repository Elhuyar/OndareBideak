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

HIZKUNTZA_CHOICES_ISV = (
    ('eu', _('Euskera')),
    ('es', _('Gaztelania')),   
    ('en', _('Ingelesa')),
)


MOTA_CHOICES = (
    (1, 'TEXT'),
    (2, 'VIDEO'),   
    (3, 'IMAGE'),
    (4, 'SOUND'),
    (5, '3D'),
)

LIZENTZIA_CHOICES = (
    (1, 'Public Domain Mark'),
    (2, 'Out of copyright - non commercial re-use'),   
    (3, 'CC0'),
    (4, 'CC-BY'),
    (5, 'CC-BY-SA'),
    (6, 'CC-BY-ND'),
    (7, 'CC-BY-NC'),
    (8, 'CC-BY-NC-SA'),
    (9, 'CC-BY-NC-ND'),
    (10, 'Rights Reserved - Free Access'),
    (11, 'Rights Reserved - Paid Access'),
    (12, 'Orphan Work'),
    (13, 'Unknown'),
)

#def get_initial_language():
    
#       return HIZKUNTZA_CHOICES[2]
 
 
class OaipmhForm(Form):
    """OAI-PMH bidez itemak datu-baseratzeko formularioa kargatzen du"""
    baseurl=CharField(max_length=150,required=True, widget=TextInput(attrs={"placeholder":_("baseUrl"),"type":"text", "class":"form-control"}))
    #wikify=BooleanField(required=False)
    
class LoginForm(Form):
    """Erabiltzaile bat logeatzeko formularioa kargatzen du"""
    erabiltzailea=CharField(max_length=150,required=True, widget=TextInput(attrs={"placeholder":_("Erabiltzailea"),"type":"text", "class":"form-control"}))
    pasahitza=CharField(max_length=32, widget=PasswordInput(attrs={"placeholder":_("Pasahitza"),"type":"password", "class":"form-control"}),required=True)

    def clean_erabiltzailea(self):
        """Erabiltzailea existitzen den konprobatzen da"""
        error_message =_("Erabiltzailea ez dago erregistratua")
        try:
            e=User.objects.get(username=self.cleaned_data["erabiltzailea"])
            return self.cleaned_data["erabiltzailea"]
        except:
            raise forms.ValidationError(error_message)

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
        
class BerriaForm(forms.Form):
    
   
    berriaid=CharField(max_length=1000,widget=TextInput(attrs={"placeholder":_("id"),"type":"text", "class":"form-control","id":"InputId","readonly":"readonly"}))
    titulua_eu=CharField(max_length=200,widget=TextInput(attrs={"placeholder":_("Titulua (EU)"),"type":"text", "class":"form-control","id":"InputTitleEU"}),required=True)
    #desk_eu=CharField(max_length=1000,widget=TextInput(attrs={"placeholder":_("Deskribapena (EU)"),"type":"text", "class":"form-control","id":"InputDeskEU"}),required=True)
    desk_eu = forms.CharField(max_length=1000,
            label = _("Deskribapena"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Deskribapena"),
                                    "rows":"3",
                                 })
    )
    
    titulua_es=CharField(max_length=200,widget=TextInput(attrs={"placeholder":_("Titulua (ES)"),"type":"text", "class":"form-control","id":"InputTitleES"}),required=False)
    #desk_es=CharField(max_length=1000,widget=TextInput(attrs={"placeholder":_("Deskribapena (ES)"),"type":"text", "class":"form-control","id":"InputDeskES"}),required=False)
    desk_es = forms.CharField(max_length=1000,
            label = _("Deskribapena"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Deskribapena"),
                                    "rows":"3",
                                 })
    )
    
    
    titulua_en=CharField(max_length=200,widget=TextInput(attrs={"placeholder":_("Titulua (EN)"),"type":"text", "class":"form-control","id":"InputTitleEN"}),required=False)
    #desk_en=CharField(max_length=1000,widget=TextInput(attrs={"placeholder":_("Deskribapena (EN)"),"type":"text", "class":"form-control","id":"InputDeskEN"}),required=False)
    desk_en = forms.CharField(max_length=1000,
            label = _("Deskribapena"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Deskribapena"),
                                    "rows":"3",
                                 })
    )
    titulua_fr=CharField(max_length=200,widget=TextInput(attrs={"placeholder":_("Titulua (FR)"),"type":"text", "class":"form-control","id":"InputTitleFR"}),required=False)
    #desk_fr=CharField(max_length=1000,widget=TextInput(attrs={"placeholder":_("Deskribapena (FR)"),"type":"text", "class":"form-control","id":"InputDeskFR"}),required=False)
    desk_fr = forms.CharField(max_length=1000,
            label = _("Deskribapena"),
            required = False,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Deskribapena"),
                                    "rows":"3",
                                 })
    )
    
    url=CharField(max_length=200,widget=TextInput(attrs={"placeholder":_("Url-a"),"type":"text", "class":"form-control","id":"InputUrl"}),required=False)
    irudia=ImageField(max_length=32,required=False)
    publikatu = forms.BooleanField(
        label = _("Publikatu"),
        required = False,
        widget=forms.CheckboxInput(attrs={"type":"check", 
                                "placeholder":_("Publikatu")
                                })
    )


class UserForm(forms.Form):
    
   
    userid=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("id"),"type":"text", "class":"form-control","id":"InputId","readonly":"readonly"}))
    izena=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Izena"),"type":"text", "class":"form-control","id":"InputName"}))
    abizena=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Abizenak"),"type":"text", "class":"form-control","id":"InputName2"}))
    username=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Erabiltzailea"),"type":"text", "class":"form-control","id":"InputUser"}))
    posta=CharField(max_length=100,widget=TextInput(attrs={"placeholder":_("Helbide elektronikoa"),"type":"text", "class":"form-control","id":"InputEmail"}))
    '''
    class Meta:
        model = User
        fields = ["id","first_name", "last_name","username", "email"]
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
      
    '''
    def clean_username(self):
        cleaned_data = self.cleaned_data
        error_message=_("Erabiltzaile izen hau dagoeneko erregistratua dago")
        if User.objects.filter(username=cleaned_data['username']).count() > 1:
            raise forms.ValidationError(error_message)
        else:
            return cleaned_data['username']
     
     
   
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
    
    hornitzailea = forms.BooleanField(
        label = _("Hornitzailea"),
        required = False,
        widget=forms.CheckboxInput(attrs={"type":"check",
                                          "class":"checkbox-inline",                                           
                                "placeholder":_("Hornitzailea")
                                }),
        help_text=_("* Kultur erakunde baten izenean zatoz? Markatu lauki hau bete hurrengo eremua. Plataformak aukera gehigarriak eskainiko dizkizu.")
                                      )
    
    
    honitzaile_izena = forms.CharField(
        label = _("Hornitzailearen izena"),
        required = False,
        widget=forms.TextInput(attrs={"type":"text", 
                                "class":"form-control",
                                "placeholder":_("Kultur item digitalen erakunde hornitzailearen izena")
                                })
    )

    
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
    
     
class ItemGehituForm(Form):
    """Item berri bat gehitzeko formularioa kargatzen du"""
    titulua=CharField(max_length=500,required=True, widget=TextInput(attrs={"placeholder":_("Titulua"),"type":"text", "class":"form-control"}))
    deskribapena=CharField(max_length=1500,required=True, widget=TextInput(attrs={"placeholder":_("Deskribapena"),"type":"text", "class":"form-control"}))
    sortzailea=CharField(max_length=300,required=False, widget=TextInput(attrs={"placeholder":_("objektu digitalaren sortzailearen izena ipini, bestela balio lehenetsi bezala 'Herritarra' agertuko da"),"type":"text", "class":"form-control"}))
    # date : momentukoa
    gaia=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("Gaia"),"type":"text", "class":"form-control"}))
    herrialdea=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("herrialdea"),"type":"text", "class":"form-control"}))
    #data = DateField(required=False,widget=TextInput(attrs={"placeholder":_("data")}))
    data = CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("Data"),"type":"text", "class":"form-control"}))
    jatorrizkoa=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("Jatorrizko Url-a"),"type":"text", "class":"form-control"}))
    eskubideak=CharField(max_length=300,required=False, widget=TextInput(attrs={"placeholder":_("Objektuaren eskubideen inguruko egin beharreko azalpenak edo kontutan hartu beharreko xehetasunak. Testu librea."),"type":"text", "class":"form-control"}))
    lizentzia=ChoiceField(required=False,  choices=LIZENTZIA_CHOICES)
    mota=ChoiceField(required=False,  choices=MOTA_CHOICES)
    #text, audio, video, image
    objektua= forms.FileField()
    irudia=ImageField(max_length=32,required=False)
    hizkuntza = forms.MultipleChoiceField(choices=HIZKUNTZA_CHOICES_ISV,widget=forms.CheckboxSelectMultiple())
       
    
class ItemEditatuForm(Form):
    """Item bat editatzeko formularioa kargatzen du"""
    titulua=CharField(max_length=500,required=True, widget=TextInput(attrs={"placeholder":_("Titulua"),"type":"text", "class":"form-control"}))
    #  sortzailea: logeatuta dagoen erabiltzailea
    deskribapena=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("Deskribapena"),"type":"text", "class":"form-control"}))
    sortzailea=CharField(max_length=300,required=False, widget=TextInput(attrs={"placeholder":_("Objektu digitalaren sortzailearen izena ipini, bestela balio lehenetsi bezala 'Herritarra' agertuko da"),"type":"text", "class":"form-control"}))
    # date : momentukoa
    gaia=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("Gaia"),"type":"text", "class":"form-control"}))
    herrialdea=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("Herrialdea"),"type":"text", "class":"form-control"}))
    #data = DateField(required=False,widget=TextInput(attrs={"placeholder":_("data")}))
    data = CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("Data"),"type":"text", "class":"form-control"}))    
    mota=ChoiceField(required=False,  choices=MOTA_CHOICES)
    #text, audio, video, image
    objektua= forms.FileField()
    jatorrizkoa=CharField(max_length=150,required=False, widget=TextInput(attrs={"placeholder":_("Jatorrizko Url-a"),"type":"text", "class":"form-control"}))  
    eskubideak=CharField(max_length=300,required=False, widget=TextInput(attrs={"placeholder":_("Objektuaren eskubideen inguruko egin beharreko azalpenak edo kontutan hartu beharreko xehetasunak. Testu librea."),"type":"text", "class":"form-control"}))
    lizentzia=ChoiceField(required=False,  choices=LIZENTZIA_CHOICES)
    irudia=ImageField(max_length=32,required=False)
    hizkuntza = forms.MultipleChoiceField(choices=HIZKUNTZA_CHOICES_ISV,widget=forms.CheckboxSelectMultiple())
    hidden_Item_id = CharField(label='reset',max_length=256, widget=forms.HiddenInput())
    
    
    
#####################
### COMMENT FORMS ###
#####################

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=500,
            label = _("Iruzkina"),
            required = True,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Iruzkina"),
                                    "rows":"3",
                                 })
    )
    


class CommentParentForm(forms.Form):
    comment = forms.CharField(max_length=500,
            label = _("Iruzkina"),
            required = True,
            widget=forms.Textarea(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Iruzkina"),
                                    "rows":"3",
                                 })
    )
    
    parent_id =forms.CharField(
            label = _("parent_id"),
            required = False,
            widget=forms.HiddenInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("parent_id"),                                    
                                 })
    )

###################
##  UPLOAD FORM  ##
###################
class UploadForm(forms.Form):
    
    file=forms.FileField(
         required=False,
         widget=forms.FileInput(attrs={"class":"form-control",
                                    "type":"file"
                                  }))
                                  

    def clean_file(self):
        image = self.cleaned_data.get('file',False)
        if image:
            if image._size > MAX_FILE_SIZE*1024*1024:
                raise ValidationError(_("Image file too large ( > "+str(MAX_FILE_SIZE)+"mb )"))
            return image
        else:
            return image


class CoordinatesForm(forms.Form):

    coordinates = forms.CharField(
            label = _("Koordenatuak"),
            required = False,
            widget=forms.HiddenInput(attrs={"type":"text", 
                                    "class":"form-control",
                                    "placeholder":_("Koordenatuak")
                                 })
    )
    

