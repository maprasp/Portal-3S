import re
from datetime import datetime
from unicodedata import normalize

from django import forms
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField

from apps.colaborador.models import VPN, Colaborador, Vinculo
from apps.core.models import ColaboradorGrupoAcesso, Divisao
from apps.core.tasks import send_email_template_task
from garb.forms import GarbForm, GarbModelForm


class EmailLowerField(forms.EmailField):
    def to_python(self, value):
        return value.lower()

class DivisaoChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.divisao} - {obj.divisao_completo}"

class SecretariaNegarForm(forms.Form):
    colaborador = forms.IntegerField(widget=forms.HiddenInput())
    motivo = forms.CharField(widget=forms.Textarea(attrs={"cols": 80, "rows": 2}))
    colaborador_obj = None

    def clean_colaborador(self):
        colaborador = self.cleaned_data.get("colaborador")
        colaborador_obj = Colaborador.objects.filter(pk=colaborador, is_active=False)
        if not colaborador_obj.exists():
            raise forms.ValidationError("Colaborador não encontrado")
        self.colaborador_obj = colaborador_obj[0]
        return colaborador

    def sendmail(self):
        context_email = [["name", self.colaborador_obj.full_name], ["motivo", self.cleaned_data.get("motivo")]]
        send_emails = [
            self.colaborador_obj.email,
            self.colaborador_obj.divisao.email,
        ]
        send_email_template_task.delay((f"Ops!!! tem algo errado no seu cadastro"), "colaborador/email/secretaria_negado.html", send_emails, context_email)
        return self.colaborador_obj


class ResponsavelNegarForm(forms.Form):
    colaborador_grupoacesso = forms.IntegerField(widget=forms.HiddenInput())
    motivo = forms.CharField(widget=forms.Textarea(attrs={"cols": 80, "rows": 2}))
    colaborador_grupoacesso_obj = None

    def clean_colaborador_grupoacesso(self):
        colaborador_grupoacesso = self.cleaned_data.get("colaborador_grupoacesso")
        colaborador_grupoacesso = ColaboradorGrupoAcesso.objects.filter(pk=colaborador_grupoacesso)
        if not colaborador_grupoacesso.exists():
            raise forms.ValidationError("Solicitação não encontrada")
        self.colaborador_grupoacesso_obj = colaborador_grupoacesso[0]
        return colaborador_grupoacesso

    def sendmail(self):
        context_email = [["name", self.colaborador_grupoacesso_obj.colaborador.full_name], ["grupo", self.colaborador_grupoacesso_obj.grupo_acesso.grupo_acesso], ["motivo", self.cleaned_data.get("motivo")]]
        send_email_template_task.delay((f"Ops!!! tem algo errado na sua solicitação"), "colaborador/email/responsavel_negado.html", [self.colaborador_grupoacesso_obj.colaborador.email], context_email)
        return self.colaborador_grupoacesso_obj


class SuporteForm(forms.ModelForm):
    email = EmailLowerField(required=True)
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Colaborador
        fields = ["id", "username", "uid", "email"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        pk = int(self.request.POST.getlist("id")[0])
        if Colaborador.objects.filter(username=username).exclude(id=pk).exists():
            messages.add_message(self.request, messages.ERROR, "Username já utilizado")
            raise forms.ValidationError("Username já utilizado", code="invalid")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        pk = int(self.request.POST.getlist("id")[0])
        if Colaborador.objects.filter(email=email).exclude(id=pk).exists():
            messages.add_message(self.request, messages.ERROR, "Email já utilizado")
            raise forms.ValidationError("Email já utilizado", code="invalid")
        return email

    def clean_uid(self):
        uid = self.cleaned_data.get("uid")
        pk = int(self.request.POST.getlist("id")[0])
        if Colaborador.objects.filter(uid=uid).exclude(id=pk).exists() or uid == 0:
            messages.add_message(self.request, messages.ERROR, "Uid não pode ser utilizado")
            raise forms.ValidationError("Uid já utilizado", code="invalid")
        return uid

    def save_sendmail(self, tmp_password, *args, **kwargs):
        colaborador = super(SuporteForm, self).save(*args, **kwargs)
        colaborador.set_password(tmp_password)
        context_email = [["name", colaborador.full_name], ["username", colaborador.username], ["password", tmp_password]]
        send_email_template_task.delay("Conta criada com sucesso!", "colaborador/email/suporte_criar.html", [colaborador.email], context_email)
        send_email_template_task.delay("Conta criada", "colaborador/email/suporte_aviso.html", [settings.EMAIL_SYSADMIN], context_email)
        messages.add_message(self.request, messages.SUCCESS, "Contra criada no portal")
        return colaborador

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)


class ColaboradorBaseForm(forms.ModelForm):
#J 
#J     documento_tipo = (
#J         ("", ""),
#J         ("RG", "RG"),
#J         ("Passaporte", "Passaporte"),
#J     )


    divisao = DivisaoChoiceField(queryset=Divisao.objects.all(), label="Divisão | Coordenação")
    responsavel = forms.ModelChoiceField(queryset=Colaborador.objects.filter(Q(groups__name="Responsavel")).distinct(), label="Responsável", widget=forms.Select(attrs={"data-live-search": "True"}),required=False,)
    last_name = forms.CharField(max_length=255, label="Sobrenome(s)")
#J    documento_tipo = forms.ChoiceField(choices=documento_tipo, label="Tipo Documento")
    email = forms.EmailField()
    class Meta:
        model = Colaborador
        fields = [
            "first_name",
            "last_name",
            "email",
#J            "data_nascimento",
#J            "telefone",
#J            "cpf",
#J            "documento_tipo",
#J            "documento",
            "vinculo",
            "predio",
            "divisao",
            "ramal",
            "responsavel",
            "data_inicio",
            "data_fim",
            "registro_inpe",
            "empresa",
            "externo",
        ]


class ColaboradorForm(ColaboradorBaseForm, GarbModelForm): 
    check_me_out1 = forms.BooleanField(required=True, label="<a href='http://s0.cptec.inpe.br/sysadmin/documentos/re518.pdf' target='_blank'>Eu li e concordo com a RE/DIR-518 Normas de uso aceit&aacute;vel dos recursos computacionais do INPE</a>")
    check_me_out2 = forms.BooleanField(required=True, label="<a href='http://s0.cptec.inpe.br/sysadmin/documentos/politica_transferencia.pdf' target='_blank'>Eu li e concordo com a Pol&iacute;tica para uso dos servi&ccedil;os de transfer&ecirc;ncia de dados da da COIDS</a>")
    check_me_out3 = forms.BooleanField(required=True, label="<a href='http://s0.cptec.inpe.br/sysadmin/documentos/politica_acesso.pdf' target='_blank'>Eu li e concordo com a Pol&iacute;tica de acesso aos Dados e Servidores da COIDS</a>")
    vinculo = forms.ModelChoiceField(queryset=Vinculo.objects.filter(Q(id__gte=2)), label="Vínculo")
    class Meta:
        model = Colaborador
        submit_text = "Enviar Informações"
        fieldsets = [
#J            ("Informações Pessoais", {"fields": ("first_name", "last_name", "email", "data_nascimento", "telefone", "cpf", "documento_tipo", "documento",)}),
            ("Informações Pessoais", {"fields": ("first_name", "last_name", "email",)}),

            ("Informações Profissionais", {"fields": ("vinculo", "predio", "divisao", "ramal", "responsavel", "data_inicio", "data_fim", "registro_inpe", "empresa", "externo")}),
            ("seus Direitos e Deveres", {"fields": ("check_me_out1", "check_me_out2", "check_me_out3")}),
        ]
    

    def save_sendmail(self, scheme=None, host=None, *args, **kwargs):
        colaborador = super(ColaboradorForm, self).save(*args, **kwargs)
        send_email_template_task.delay("Seu cadastro foi enviado para secretaria", "colaborador/email/colaborador_cadastro.html", [colaborador.email], [["colaborador", colaborador.full_name]])
        context_email = [["name", colaborador.full_name], ["divisao", colaborador.divisao.divisao], ["scheme", scheme], ["host", host]]
        if colaborador.responsavel:
            send_email_template_task.delay("Você é responsavel por um Colaborador", "colaborador/email/colaborador_responsavel.html", [colaborador.responsavel.email], [["colaborador", colaborador.full_name]])
        send_email_template_task.delay((f"Termo do {colaborador.full_name} para imprimir e assinar"), "colaborador/email/colaborador_termo.html", [colaborador.divisao.email,], context_email)
        return colaborador

class VPNForm(forms.ModelForm):
    JUSTIFICATIVA_CHOICES =( 
        ("",""),
        ("SOLICITAÇÃO de Conta VPN Colaborador | Interno", "SOLICITAÇÃO de Conta VPN Colaborador | Interno"), 
        ("SOLICITAÇÃO de Conta VPN Colaborador | Interno", "SOLICITAÇÃO de Conta VPN Colaborador | Externo"), 
        ("REVALIDAÇÃO de Conta VPN", "REVALIDAÇÃO de Conta VPN"), 
        ("REMOÇÃO de Conta VPN", "REMOÇÃO de Conta VPN"), 
        ("ADIÇÃO de equipamento com VPN ativa", "ADIÇÃO de equipamento com VPN ativa"), 
        ("TROCA de equipamento com VPN ativa", "TROCA de equipamento com VPN ativa"), 
        ("REMOÇÃO de equipamento com VPN ativa", "REMOÇÃO de equipamento com VPN ativa"), 

    ) 
    RECURSO_CHOICES = (
        ("",""),
        ("VPN-CPTEC | Rede OPERACIONAL – 147", "VPN-CPTEC | Rede OPERACIONAL – 147"),
        ("VPN-CPTEC | Rede PESQUISA | DESENVOLVIMENTO – 149", "VPN-CPTEC | Rede PESQUISA | DESENVOLVIMENTO – 149"),
        ("VPN-HPC | Super – TUPA", "VPN-HPC | Super – TUPA"),
        ("VPN-HPC | Super – XC-50", "VPN-HPC | Super – XC-50"),
        ("VPN-HPC | Kerana", "VPN-HPC | Kerana"),
        ("VPN-HPC | Argos", "VPN-HPC | Argos"),
        ("VPN-HPC | Jaguar", "VPN-HPC | Jaguar"),
        ("VPN-HPC | Laquibrido", "VPN-HPC | Laquibrido"),
    )

    justificativa = forms.ChoiceField(choices = JUSTIFICATIVA_CHOICES) 
    recurso = forms.ChoiceField(choices = RECURSO_CHOICES) 
    

    class Meta:
        model = VPN
        fields = "__all__"
        widgets = {"colaborador": forms.Select(attrs={"data-live-search": "True"})}
    


class ColaboradorExternoForm(GarbForm):
    email = forms.EmailField(required=True)
    class Meta:
        fieldsets = [
            ("Solicitar Informações do Colaborador Externo", {"fields": ("email",)}),
        ]
