from django import forms
from django.contrib.auth.forms import AuthenticationForm

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
