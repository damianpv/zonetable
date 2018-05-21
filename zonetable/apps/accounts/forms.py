# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from datetime import datetime

from zonetable.apps.home.models import Language, State, Country
from zonetable.apps.directory.models import Category
from zonetable.apps.accounts.models import UserProfile

NAC_DIA_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21'),
    ('22', '22'),
    ('23', '23'),
    ('24', '24'),
    ('25', '25'),
    ('26', '26'),
    ('27', '27'),
    ('28', '28'),
    ('29', '29'),
    ('30', '30'),
    ('31', '31'),
)

NAC_MES_CHOICES = (
    ('01', 'Enero'),
    ('02', 'Febrero'),
    ('03', 'Marzo'),
    ('04', 'Abril'),
    ('05', 'Mayo'),
    ('06', 'Junio'),
    ('07', 'Julio'),
    ('08', 'Agosto'),
    ('09', 'Septiembre'),
    ('10', 'Octubre'),
    ('11', 'Noviembre'),
    ('12', 'Diciembre'),
)

SELECCIONE_CHOICES = (
    ('', 'Seleccione uno'),
)

class LoginForm(forms.Form):
    #Email = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-xlarge','placeholder':'Inserte su Email...'}))
    #Password    = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge','placeholder':u'Inserte su Teléfono...'}))
    email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class ForgotPassForm(forms.Form):
    forgot_email = forms.CharField(widget=forms.TextInput())

# Registro
class UserForm(forms.ModelForm):
    email       = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-xlarge','placeholder':u'Inserte su Email...', 'tabindex':'1'}), error_messages={'required': 'Campo obligatorio'})
    password    = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class':'input-xlarge','placeholder':u'Inserte su contraseña...', 'tabindex':'2'}), error_messages={'required': 'Campo obligatorio'})
    repassword  = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class':'input-xlarge','placeholder':u'Repita su contraseña...', 'tabindex':'3'}), error_messages={'required': 'Campo obligatorio'})

    first_name  = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'4', 'autofocus':'autofocus'}), error_messages={'required': 'Campo obligatorio'})
    last_name   = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'5'}), error_messages={'required': 'Campo obligatorio'})

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        num_words = len(password)
        if num_words < 5:
            raise forms.ValidationError('Debe tener más 5 caracteres.')
        return password

    def clean_repassword(self):
        password = self.cleaned_data.get('password', '')
        repassword = self.cleaned_data.get('repassword', '')

        if password != repassword:
            raise forms.ValidationError('No coinciden.')
        return repassword
    
    class Meta:
        model = User
        exclude = {'username', 'repassword', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined'}

# Registro y Perfil
class RegisterForm(forms.ModelForm):

    year_start = datetime.now().year-100
    year_end = datetime.now().year-18
    NAC_ANIO_CHOICES = [(x, x) for x in range(year_start, year_end)]

    address          = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'6','placeholder':u'Inserte su Dirección...'}))
    phone            = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'6','placeholder':u'Inserte su Teléfono...'}))
    birth_day        = forms.CharField(required=False,widget=forms.Select(choices=NAC_DIA_CHOICES, attrs={'class':'nac_dia', 'tabindex':'7'}))
    birth_month      = forms.CharField(required=False,widget=forms.Select(choices=NAC_MES_CHOICES, attrs={'class':'nac_mes', 'tabindex':'8'}))
    birth_year       = forms.CharField(required=False,widget=forms.Select(choices=NAC_ANIO_CHOICES, attrs={'class':'nac_anio', 'tabindex':'9'}))
    #estado          = forms.CharField(widget=forms.Select(choices=SELECCIONE_CHOICES, attrs={'disabled':'disabled', 'tabindex':'8'}), error_messages={'required': 'Campo obligatorio'})
    country          = forms.ModelChoiceField(queryset = Country.objects.all().filter(status=True), widget=forms.Select(attrs={'tabindex':'10'}), error_messages={'required': 'Campo obligatorio'})
    state            = forms.ModelChoiceField(queryset = State.objects.all().filter(status=True), widget=forms.Select(attrs={'tabindex':'11'}), error_messages={'required': 'Campo obligatorio'})
    language         = forms.ModelChoiceField(queryset = Language.objects.all().filter(status=True), widget=forms.Select(attrs={'style': u'width: 250px', 'tabindex':'12'}), error_messages={'required': 'Campo obligatorio'})
    #pais            = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label=u'País', error_messages={'required':'Campo obligatorio'}, label=u'País.', widget=forms.Select(attrs={'tabindex':'6'}))
    #pais	 	     = forms.IntegerField(widget=forms.Select(choices=Country.objects.all().values_list('id_country','country'), attrs={'tabindex':'7'}))
    #Estado          = forms.ModelChoiceField(queryset=State.objects.all(), empty_label=u'Estado', error_messages={'required':'Campo obligatorio'}, label=u'Estado.', widget=forms.Select(attrs={'tabindex':'6','style':'width:285px'}))
    category         = forms.ModelMultipleChoiceField(queryset=Category.objects.all().filter(status=True), widget=forms.SelectMultiple(attrs={'placeholder': u'Inserte ...', 'style':'width:526px', 'tabindex':'12'}), error_messages={'required': 'Campo obligatorio'})
    terms_conditions = forms.BooleanField(required=True, error_messages={'required': 'Por favor, confirma que has leído y aceptado los términos y condiciones del sitio.'})

    class Meta:
        model = UserProfile
        exclude = {'user', 'random', 'user_status', 'fb_id', 'fb_verify', 'gender', 'locale', 'birthday'}

# Editar: Perfil de usuario
class ProfileForm(forms.ModelForm):
    password    = forms.CharField(required=False, widget=forms.PasswordInput(render_value=False, attrs={'class':'input-xlarge','placeholder':u'Inserte su contraseña...', 'tabindex':'1'}), error_messages={'required': 'Campo obligatorio'})
    repassword  = forms.CharField(required=False, widget=forms.PasswordInput(render_value=False, attrs={'class':'input-xlarge','placeholder':u'Repita su contraseña...', 'tabindex':'2'}), error_messages={'required': 'Campo obligatorio'})
    first_name  = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'3', 'autofocus':'autofocus'}), error_messages={'required': 'Campo obligatorio'})
    last_name   = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'4'}), error_messages={'required': 'Campo obligatorio'})

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        num_words = len(password)
        if num_words > 0:
            if num_words < 5:
                raise forms.ValidationError('Debe tener más 5 caracteres.')
            return password

    def clean_repassword(self):
        password = self.cleaned_data.get('password', '')
        repassword = self.cleaned_data.get('repassword', '')
        
        r_num_words = len(repassword)

        if r_num_words > 0:
            if password != repassword:
                raise forms.ValidationError('No coincide.')
            return repassword
    
    class Meta:
        model = User
        exclude = {'username', 'email', 'password', 'repassword', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined'}

# Perfil
class EditRegisterForm(forms.ModelForm):

    year_start = datetime.now().year-100
    year_end = datetime.now().year-18
    NAC_ANIO_CHOICES = [(x, x) for x in range(year_start, year_end)]

    address          = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'6','placeholder':u'Inserte su Dirección...'}))
    phone            = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'6','placeholder':u'Inserte su Teléfono...'}))
    birth_day        = forms.CharField(required=False,widget=forms.Select(choices=NAC_DIA_CHOICES, attrs={'class':'nac_dia', 'tabindex':'7'}))
    birth_month      = forms.CharField(required=False,widget=forms.Select(choices=NAC_MES_CHOICES, attrs={'class':'nac_mes', 'tabindex':'8'}))
    birth_year       = forms.CharField(required=False,widget=forms.Select(choices=NAC_ANIO_CHOICES, attrs={'class':'nac_anio', 'tabindex':'9'}))
    #estado          = forms.CharField(widget=forms.Select(choices=SELECCIONE_CHOICES, attrs={'disabled':'disabled', 'tabindex':'8'}), error_messages={'required': 'Campo obligatorio'})
    country          = forms.ModelChoiceField(queryset = Country.objects.all().filter(status=True), widget=forms.Select(attrs={'tabindex':'10'}), error_messages={'required': 'Campo obligatorio'})
    state            = forms.ModelChoiceField(queryset = State.objects.all().filter(status=True), widget=forms.Select(attrs={'tabindex':'11'}), error_messages={'required': 'Campo obligatorio'})
    language         = forms.ModelChoiceField(queryset = Language.objects.all().filter(status=True), widget=forms.Select(attrs={'style': u'width: 250px', 'tabindex':'12'}), error_messages={'required': 'Campo obligatorio'})
    #pais            = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label=u'País', error_messages={'required':'Campo obligatorio'}, label=u'País.', widget=forms.Select(attrs={'tabindex':'6'}))
    #pais            = forms.IntegerField(widget=forms.Select(choices=Country.objects.all().values_list('id_country','country'), attrs={'tabindex':'7'}))
    #Estado          = forms.ModelChoiceField(queryset=State.objects.all(), empty_label=u'Estado', error_messages={'required':'Campo obligatorio'}, label=u'Estado.', widget=forms.Select(attrs={'tabindex':'6','style':'width:285px'}))
    category         = forms.ModelMultipleChoiceField(queryset=Category.objects.all().filter(status=True), widget=forms.SelectMultiple(attrs={'placeholder': u'Inserte ...', 'style':'width:526px', 'tabindex':'12'}), error_messages={'required': 'Campo obligatorio'})

    class Meta:
        model = UserProfile
        exclude = {'user', 'random', 'user_status', 'fb_id', 'fb_verify', 'gender', 'locale', 'birthday', 'terms_conditions'}

'''
class ProfileForm(forms.Form):
    nombre      = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'1', 'autofocus':'autofocus'}), error_messages={'required': 'Campo obligatorio'})
    apellidos   = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'2'}), error_messages={'required': 'Campo obligatorio'})
    telefono    = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'3','placeholder':u'Inserte su Teléfono...'}))
    nac_dia     = forms.CharField(required=False, widget=forms.Select(choices=NAC_DIA_CHOICES, attrs={'class':'nac_dia', 'tabindex':'4'}))
    nac_mes     = forms.CharField(required=False, widget=forms.Select(choices=NAC_MES_CHOICES, attrs={'class':'nac_mes', 'tabindex':'5'}))
    nac_anio    = forms.CharField(required=False, widget=forms.Select(choices=NAC_ANIO_CHOICES, attrs={'class':'nac_anio', 'tabindex':'6'}))
    #estado     = forms.CharField(widget=forms.Select(choices=SELECCIONE_CHOICES, attrs={'disabled':'disabled', 'tabindex':'8'}), error_messages={'required': 'Campo obligatorio'})
    estado        = forms.ModelChoiceField(queryset = State.objects.all().filter(status=True))

    pais        = forms.ModelChoiceField(queryset = Country.objects.all().filter(status=True))
    #pais        = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label=u'País', error_messages={'required':'Campo obligatorio'}, label=u'País.', widget=forms.Select(attrs={'tabindex':'6'}))
    #pais       = forms.IntegerField(widget=forms.Select(choices=Country.objects.all().values_list('id_country','country'), attrs={'tabindex':'7'}))
    #Estado     = forms.ModelChoiceField(queryset=State.objects.all(), empty_label=u'Estado', error_messages={'required':'Campo obligatorio'}, label=u'Estado.', widget=forms.Select(attrs={'tabindex':'6','style':'width:285px'}))
    email       = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-xlarge','placeholder':u'Inserte su Email...', 'tabindex':'9', 'readonly':'readonly'}), error_messages={'required': 'Campo obligatorio'})
    password    = forms.CharField(required=False, widget=forms.PasswordInput(render_value=False, attrs={'class':'input-xlarge','placeholder':u'Inserte su contraseña...', 'tabindex':'10'}), error_messages={'required': 'Campo obligatorio'})
    repassword  = forms.CharField(required=False, widget=forms.PasswordInput(render_value=False, attrs={'class':'input-xlarge','placeholder':u'Repita su contraseña...', 'tabindex':'11'}), error_messages={'required': 'Campo obligatorio'})

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        num_words = len(password)
        if num_words > 0:
            if num_words < 5:
                raise forms.ValidationError('Debe tener más 5 caracteres.')
            return password

    def clean_repassword(self):
        password = self.cleaned_data.get('password', '')
        repassword = self.cleaned_data.get('repassword', '')
        
        r_num_words = len(repassword)

        if r_num_words > 0:
            if password != repassword:
                raise forms.ValidationError('La contraseña no coincide.')
            return repassword
'''
