from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import ReporteDano, UsuarioTransportista, PiezaRechazada, Pieza, CategoriaDano, Cliente

class FlexibleLoginForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        # Personalización del mensaje de error general
        self.error_messages.update({
            'invalid_login': "Contraseña o Usuario incorrectos.",
        })

        # Personalización de mensajes de campos obligatorios
        for field in self.fields:
            self.fields[field].error_messages['required'] = f"El campo {field} es obligatorio."

class ReporteDanoForm(forms.ModelForm):
    # --- Campos de Usuario Transportista ---
    transporte = forms.ChoiceField(
        label='Transporte',
        choices=UsuarioTransportista.OPCIONES_TRANSPORTE,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    dniConductor = forms.CharField(
        label='DNI',
        max_length=10, 
        min_length=7,
        widget=forms.TextInput(attrs={
            'placeholder': "Ej: 22.312.341",
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
            'class': 'form-control'
        })
    )

    nombreConductor = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Ej: Juan',
        'class': 'form-control'
    }))

    apellidoConductor = forms.CharField(label='Apellido', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Ej: Romero ',
        'class': 'form-control'
    }))

    patenteConductor = forms.CharField(label='Patente', max_length=20, widget=forms.TextInput(attrs={
        'placeholder': 'Ej: AF482CK / KTO915 ',
        'class': 'form-control'
    }))

    class Meta:
        model = ReporteDano
        fields = ['empleado', 'cliente']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mensajes_personalizados = {
            'empleado': 'El Empleado es obligatorio.',
            'cliente': 'El Cliente es obligatorio.',
            'dniConductor': 'El DNI es obligatorio.',
            'nombreConductor': 'El Nombre es obligatorio.',
            'apellidoConductor': 'El Apellido es obligatorio.',
            'patenteConductor': 'La Patente es obligatoria.',
            'transporte': 'Seleccione el tipo de Transporte.',
        }

        for field_name, mensaje in mensajes_personalizados.items():
            if field_name in self.fields:
                self.fields[field_name].required=True
                self.fields[field_name].error_messages['required'] = mensaje

    # --- Validación y Limpieza de los datos de Usuario Transportista ---
    def clean_dniConductor(self):
        dni_crudo = self.cleaned_data.get('dniConductor', '')
        dni_limpio = dni_crudo.replace('.', '').strip()

        if not dni_limpio.isdigit():
            raise ValidationError('El DNI debe contener únicamente números.')
        if len (dni_limpio) < 7 or len(dni_limpio) > 8:
            raise ValidationError('El DNI debe tener entre 7 u 8 dígitos.')
        
        return dni_limpio
    
    def clean_patenteConductor(self):
        patente_cruda = self.cleaned_data.get('patenteConductor', '')
        patente_limpia = patente_cruda.replace(' ', '').strip().upper()

        return patente_limpia
    
    def clean_nombreConductor(self):
        return self.cleaned_data.get('nombreConductor', '').strip().lower()
    
    def clean_apellidoConductor(self):
        return self.cleaned_data.get('apellidoConductor', '').strip().lower()
    
class PiezaRechazadaForm(forms.ModelForm):
    pieza = forms.ModelChoiceField(
        label="Pieza",
        queryset=Pieza.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    categoria_dano = forms.ModelChoiceField(
        label='Tipo de Daño',
        queryset=CategoriaDano.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    cantidad = forms.IntegerField(
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'inputmode': 'numeric'})
    )

    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'capture': 'environment', 'accept': 'image/*'})
    )

    class Meta:
        model = PiezaRechazada
        fields = ['pieza', 'categoria_dano', 'cantidad', 'observaciones', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pieza'].required=True
        self.fields['categoria_dano'].required=True
        self.fields['cantidad'].required=True
        self.fields['imagen'].required=True

        if self.instance.pk and self.instance.imagen:
            self.fields['imagen'].required=False


        mensajes = {
            'pieza': 'Seleccione una pieza.',
            'categoria_dano': 'Indique el tipo de daño.',
            'cantidad': 'Ingrese una cantidad válida.',
            'imagen': 'La foto de la pieza es obligatoria.'
        }

        for field_name, field in self.fields.items():
            if field_name != 'observaciones':
                field.required = True
            if field_name in mensajes:
                field.widget.attrs['data-error-msg'] = mensajes[field_name]

PiezasFormSet = inlineformset_factory(
    ReporteDano,
    PiezaRechazada,
    form=PiezaRechazadaForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)

class ClienteForm(forms.ModelForm):
    nombre = forms.CharField(
        label='Razon Social',
        error_messages={
            'required': 'La razón social es obligatoria.'
        },
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ECVA SRL'})
    )

    mail = forms.EmailField(
        label='Correo Electrónico',
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'invalid': 'Por favor, ingrese una dirección de correo válida.',
            'unique': 'Este correo ya se encuentra registrado.'
        },
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )

    domicilio = forms.CharField(
        label='Domicilio',
        error_messages={
            'required': 'El domicilio es obligatorio.'
        },
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. Teodoro Planas 1245'})
    )

    telefono = forms.CharField(
        label='Teléfono / Celular',
        max_length=11,
        min_length=10,
        error_messages={
            'required': 'El número de teléfono es obligatorio.',
            'min_length': 'El teléfono debe tener al menos 10 dígitos.',
            'max_length': 'El teléfono no puede superar los 11 dígitos.'
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 299155XXXX',
            'inputmode': 'numeric',
            'pattern': '[0-9]{10,11}',
            'class': 'form-control'
        }))
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'mail', 'domicilio']

    def clean_nombre(self):
        return self.cleaned_data.get('nombre', '').strip().lower()
    
    def clean_domicilio(self):
        return self.cleaned_data.get('domicilio', '').strip().lower()
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números, sin espacios ni guiones.")
        return telefono
        
    
    
    
