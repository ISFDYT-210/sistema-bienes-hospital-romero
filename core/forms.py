# core/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from core.models import BienPatrimonial
from core.models.expediente import Expediente
from datetime import date

# ========== FORMULARIO DE CARGA MASIVA ==========
class CargaMasivaForm(forms.Form):
    archivo_excel = forms.FileField(
        label='Seleccionar archivo Excel',
        help_text='Formatos soportados: .xlsx, .xls',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    sector = forms.CharField(
        max_length=100,
        required=False,
        label='Sector por defecto (opcional)',
        help_text='Si se deja vacío, se tomará el sector de cada fila del archivo.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


# ========== FORMULARIO DE BIENES PATRIMONIALES ==========
class BienPatrimonialForm(forms.ModelForm):
    numero_expediente = forms.CharField(label="N° de Expediente", max_length=50, required=False)
    numero_compra     = forms.CharField(label="N° de Compra",     max_length=50, required=False)

    class Meta:
        model = BienPatrimonial
        fields = [
            'descripcion', 'cantidad', 'expediente', 'cuenta_codigo', 'nomenclatura_bienes',
            'numero_serie', 'numero_identificacion', 'numero_compra', 'origen', 'estado', 'servicios',
            'observaciones', 'siem', 'valor_adquisicion', 'fecha_adquisicion', 'fecha_baja',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'expediente': forms.Select(attrs={'class': 'form-select'}),
            'cuenta_codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nomenclatura_bienes': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_compra': forms.TextInput(attrs={'class': 'form-control'}),
            'origen': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'servicios': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'siem': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'valor_adquisicion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_baja': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["numero_expediente"].widget.attrs.setdefault("class", "form-control")
        self.fields["numero_compra"].widget.attrs.setdefault("class", "form-control")
        self.fields["numero_expediente"].widget.attrs.setdefault("placeholder", "Ej: EX-123/2025")
        self.fields["numero_compra"].widget.attrs.setdefault("placeholder", "Ej: OC-45/2025")
        exp = getattr(self.instance, "expediente", None)
        if exp:
            self.fields["numero_expediente"].initial = exp.numero_expediente
            if not self.instance.numero_compra:
                self.fields["numero_compra"].initial = exp.numero_compra

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("origen") and cleaned["origen"] != "COMPRA":
            cleaned["valor_adquisicion"] = None
        estado = cleaned.get("estado")
        fecha_baja = cleaned.get("fecha_baja")
        if estado == "BAJA":
            if not fecha_baja:
                cleaned["fecha_baja"] = date.today()
        else:
            cleaned["fecha_baja"] = None
        return cleaned

    def save(self, commit=True):
        bien = super().save(commit=False)
        n_exp = (self.cleaned_data.get("numero_expediente") or "").strip()
        n_cmp = (self.cleaned_data.get("numero_compra") or "").strip()
        if n_exp:
            expediente, _ = Expediente.objects.get_or_create(numero_expediente=n_exp)
            if n_cmp and (not expediente.numero_compra or expediente.numero_compra != n_cmp):
                expediente.numero_compra = n_cmp
                expediente.save()
        else:
            expediente = self.cleaned_data.get("expediente")
        bien.expediente = expediente
        if commit:
            bien.save()
            self.save_m2m()
        return bien


# ========== FORMULARIO DE OPERADORES ==========
class OperadorForm(forms.Form):
    nombre = forms.CharField(max_length=200, required=True, label='Nombre')
    apellido = forms.CharField(max_length=200, required=True, label='Apellido')
    pais = forms.CharField(max_length=100, required=False, label='País')
    dni = forms.CharField(
        max_length=8,
        required=True,
        label='DNI',
        validators=[
            RegexValidator(r'^\d{1,8}$', 'El DNI debe tener sólo números y hasta 8 dígitos.')
        ]
    )
    email = forms.EmailField(required=False, label='Email')
    estado = forms.ChoiceField(
        choices=[('habilitado', 'Habilitado'), ('no-habilitado', 'No Habilitado')],
        initial='habilitado',
        label='Estado'
    )
    tipo_usuario = forms.ChoiceField(
        choices=[('operador', 'Operador'), ('supervisor', 'Supervisor')],
        initial='operador',
        label='Tipo de Usuario'
    )
    password = forms.CharField(required=False, widget=forms.PasswordInput, label='Contraseña')

    def __init__(self, *args, operador_pk=None, **kwargs):
        self.operador_pk = operador_pk
        super().__init__(*args, **kwargs)
        if self.operador_pk:
            self.fields['dni'].required = False

    def clean_dni(self):
        dni = (self.cleaned_data.get('dni') or '').strip()
        if not dni:
            return dni
        if not dni.isdigit() or len(dni) > 8:
            raise ValidationError('El DNI debe tener sólo números y hasta 8 dígitos.')
        Operador = get_user_model()
        operadores = Operador.objects.filter(numero_doc__iexact=dni)
        if self.operador_pk:
            operadores = operadores.exclude(pk=self.operador_pk)
        if operadores.exists():
            raise ValidationError('Ya existe un operador con ese DNI')
        return dni

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if not email:
            return email
        Operador = get_user_model()
        operadores = Operador.objects.filter(email__iexact=email)
        if self.operador_pk:
            operadores = operadores.exclude(pk=self.operador_pk)
        if operadores.exists():
            raise ValidationError('Ya existe un operador con ese email')
        return email