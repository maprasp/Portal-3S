#!../env/bin/python3

import datetime
import getpass
import os
import sys
import django
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


def password():
    password_field = None
    while password_field is None:
        password = getpass.getpass()
        password2 = getpass.getpass("Password (again): ")
        if password != password2:
            print("Error: Your passwords didn't match.")
            # Don't validate passwords that don't match.
            continue
        if password.strip() == "":
            print("Error: Blank passwords aren't allowed.")
            # Don't validate blank passwords.
            continue
        try:
            validate_password(password2)
        except exceptions.ValidationError as err:
            print("\n".join(err.messages))
            response = input("Bypass password validation and create user anyway? [y/N]: ")
            if response.lower() != "y":
                continue
        password_field = password
    return password_field


def set_predio():
    from apps.core.models import Predio

    predio = Predio()
    predio.predio = "CPTEC"
    predio.predio_sistema = "CPT"
    predio.linhas = 46
    predio.colunas = 66
    predio.sensores = 16
    predio.areas = "(1, 36, 1, 19)/(36, 43, 1, 4)/(43, 46, 1, 30)"
    predio.save()


def set_divisao():
    from apps.core.models import Divisao

    organograma = (
        {
            "divisao": "CGCT",
            "divisao_completo": "Coordenação Geral de Ciências da Terra",
            "coordenacao": "CGCT - Coordenação Geral de Ciências da Terra",
        },
        {
            "divisao": "DIMNT",
            "divisao_completo": "Divisão de Modelagem Numérica do Sistema Terrestre",
            "coordenacao": "CGCT - Coordenação Geral de Ciências da Terra",
        },
        {
            "divisao": "DIPTC",
            "divisao_completo": "Divisão de Previsão de Tempo e Clima",
            "coordenacao": "CGCT - Coordenação Geral de Ciências da Terra",
        },
        {
            "divisao": "DISSM",
            "divisao_completo": "Divisão de Satélites e Sensores Meteorológicos",
            "coordenacao": "CGCT - Coordenação Geral de Ciências da Terra",
        },
        {
            "divisao": "DIIAV",
            "divisao_completo": "Divisão de Impactos, Adaptação e Vulnerabilidades",
            "coordenacao": "CGCT - Coordenação Geral de Ciências da Terra",
        },
        {
            "divisao": "SESUP",
            "divisao_completo": "Serviço de Supercomputação",
            "coordenacao": "COIDS - Coordenação de Infraestrutura de Dados e Supercomputação",
        },
        {
            "divisao": "ICT",
            "divisao_completo": "Infraestrutura Científica e Tecnológica",
            "coordenacao": "COIDS - Coordenação de Infraestrutura de Dados e Supercomputação",
        },
        {
            "divisao": "COPDT",
            "divisao_completo": "Coordenação de Pesquisa Aplicada e Desenvolvimento Tecnológico",
            "coordenacao": "COPDT - Coordenação de Pesquisa Aplicada e Desenvolvimento Tecnológico",
        },
        {
            "divisao": "DIOTG",
            "divisao_completo": "Divisão de Observação da Terra e Geoinformática",
            "coordenacao": "COPDT - Coordenação de Pesquisa Aplicada e Desenvolvimento Tecnológico",
        },
        {
            "divisao": "DIPE2",
            "divisao_completo": "Divisão de Projeto Estratégico 2",
            "coordenacao": "COGPI - Coordenação de Gestão de Projetos e Inovação Tecnológica",
        },
        {
            "divisao": "COIDS",
            "divisao_completo": "Coordenação de Infraestrutura de Dados e Supercomputação",
            "coordenacao": "COIDS - Coordenação de Infraestrutura de Dados e Supercomputação",
        },
    )
    for divisao in organograma:
        obj_divisao = Divisao()
        obj_divisao.divisao = divisao["divisao"]
        obj_divisao.divisao_completo = divisao["divisao_completo"]
        obj_divisao.coordenacao = divisao["coordenacao"]
        obj_divisao.email = "super.sesup@inpe.br"
        obj_divisao.save()


def set_vinculo():
    from apps.colaborador.models import Vinculo

    vinculos = (
        "Administrador",
        "Bolsista",
        "Servidor",
        "Terceiro",
        "Estagiário",
    )
    for vinculo_name in vinculos:
        vinculo = Vinculo(vinculo=vinculo_name)
        vinculo.save()


def set_permissoes():
    from django.contrib.auth.models import Group, Permission

    permission_suporte = [
                "add_grupotrabalho",
                "change_grupotrabalho",
                "delete_grupotrabalho",
                "view_grupotrabalho",
                "add_responsavelgrupotrabalho",
                "change_responsavelgrupotrabalho",
                "delete_responsavelgrupotrabalho",
                "view_responsavelgrupotrabalho",
                "view_grupoacesso",
                "view_colaboradorgrupoacesso",
                "view_equipamento",
                "add_rack",
                "change_rack",
                "delete_rack",
                "view_rack",
                "add_servidor",
                "change_servidor",
                "delete_servidor",
                "view_servidor",
                "view_supercomputador",
                "view_storageareagrupotrabalho",
                "add_ocorrencia",
                "change_ocorrencia",
                "delete_ocorrencia",
                "view_ocorrencia",
                "add_hostnameip",
                "change_hostnameip",
                "delete_hostnameip",
                "view_hostnameip",
                "add_equipamentogrupoacesso",
                "change_equipamentogrupoacesso",
                "delete_equipamentogrupoacesso",
                "view_equipamentogrupoacesso",
                "view_storagegrupoacessomontagem",
                "add_servidorhostnameip",
                "change_servidorhostnameip",
                "delete_servidorhostnameip",
                "view_servidorhostnameip",
                "add_equipamentoparte",
                "change_equipamentoparte",
                "delete_equipamentoparte",
                "view_equipamentoparte",
                "change_colaborador",
                "view_colaborador",
                "suporte_colaborador",
                "view_storagearea",
                "add_storagearea",
                "change_storagearea",
                "delete_storagearea",
                "add_storageareagrupotrabalho",
                "change_storageareagrupotrabalho",
                "delete_storageareagrupotrabalho",
                "view_storageareagrupotrabalho",
                "add_documento",
                "change_documento",
                "delete_documento",
                "view_documento",
            ]
        
    permission_servicedesk = permission_suporte.copy()
    permission_servicedesk.extend(["view_vpn","add_vpn","change_vpn","delete_vpn"])
    permission_suporte.extend(["add_templatevm","change_templatevm","delete_templatevm","view_templatevm","add_templatehostnameip", "change_templatehostnameip", "delete_templatehostnameip","view_templatehostnameip","add_templatecomando", "change_templatecomando","delete_templatecomando","view_templatecomando",])

    permission_default = (
        {"grupo": "Secretaria", "permission": ["change_divisao", "view_divisao", "view_colaborador", "change_colaborador", "secretaria_colaborador","view_vpn","add_vpn","add_documento",  "change_documento", "delete_documento", "view_documento", ]},
        {"grupo": "Servicedesk", "permission": permission_servicedesk, },
        {"grupo": "Colaborador", "permission": []},
        {"grupo": "Responsável", "permission": ["responsavel_colaborador"]},
        {"grupo": "NOC", "permission": ["view_colaborador", "view_servidor","view_supercomputador","view_storageareagrupotrabalho","view_equipamentogrupoacesso","view_storagearea","view_servidorhostnameip","view_hostnameip", "view_rack", "add_ocorrencia",
        "change_ocorrencia", "delete_ocorrencia", "view_ocorrencia","view_servidorhostnameip","view_storagearea","view_equipamentoparte",]},
        {"grupo": "Chefia da Divisão", "permission": ["chefia_colaborador"]},
        {"grupo": "Supercomputação", "permission": permission_suporte},
        {"grupo": "3SWiki", "permission": []},
    )

    for grupo in permission_default:
        obj_grupo = Group()
        obj_grupo.name = grupo["grupo"]
        obj_grupo.save()
        for permission in grupo["permission"]:
            print(f"add {permission} in {grupo['grupo']}")
            obj_grupo.permissions.add(Permission.objects.get(codename=permission))
        obj_grupo.save()


def set_colaborador():
    from apps.colaborador.models import Colaborador, Vinculo
    from apps.core.models import Divisao
    from django.contrib.auth.models import Group

    colaborador = Colaborador()
    colaborador.username = "admin.portal"
    colaborador.email = "super.sesup@inpe.br"
    colaborador.first_name = "Administrador"
    colaborador.last_name = "do Portal"
    colaborador.data_nascimento = datetime.date.today()
    colaborador.telefone = "(12) 3186-8476"
    colaborador.ramal = "8476"
    colaborador.documento = "."
    colaborador.documento_tipo = "RG"
    colaborador.predio_id = 1
    colaborador.data_inicio = datetime.date.today()
    colaborador.divisao = Divisao.objects.get(divisao="SESUP")
    colaborador.vinculo = Vinculo.objects.get(vinculo="Administrador")
    colaborador.set_password(password())
    colaborador.save()
    colaborador.is_superuser = True
    colaborador.is_active = True
    colaborador.is_staff = True
    colaborador.save()
    print(f"colaborador Save")

    colaborador.groups.add(Group.objects.get(name="Responsável"))
    colaborador.groups.add(Group.objects.get(name="Secretaria"))
    colaborador.groups.add(Group.objects.get(name="NOC"))
    colaborador.groups.add(Group.objects.get(name="Servicedesk"))
    colaborador.groups.add(Group.objects.get(name="Supercomputação"))
    colaborador.groups.add(Group.objects.get(name="Colaborador"))
    colaborador.groups.add(Group.objects.get(name="Chefia da Divisão"))
    colaborador.groups.add(Group.objects.get(name="3SWiki"))
    colaborador.save()
    print(f"colaborador add Groups")

    for divisao in Divisao.objects.all():
        divisao.chefe = colaborador
        divisao.chefe_substituto = colaborador
        divisao.save()


if __name__ == "__main__":
    sys.path.append(os.path.abspath("./"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ["django_settings_module"])
    django.setup()
    print("\n\n#### criando prédio\n")
    set_predio()
    print("#### criando vínculo\n")
    set_vinculo()
    print("#### criando divisão\n")
    set_divisao()
    print("#### criando permissão")
    set_permissoes()
    print("#### criando colaborador\n")
    print("#### Digite a Senha:")
    set_colaborador()