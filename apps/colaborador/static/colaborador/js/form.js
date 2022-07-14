
///// função para corrigir os campos que somem do vinculo
function combo_vinculo() {
    if ($('#id_vinculo').length)  {
        $(".field-data_fim").hide();
        $(".field-empresa").hide();
        $(".field-registro_inpe").hide();
        $(".field-responsavel").hide();
        if ($('#id_vinculo').val() === '') { return; }
        if ($('#id_vinculo option:selected').text() == "Servidor" || $('#id_vinculo').val() == "Servidor" ) {  //se for servidor
            $(".field-registro_inpe").show();
            $('#id_registro_inpe').rules('add', { required: true });
            $('#id_responsavel').rules( "remove" );
        } else if ($('#id_vinculo option:selected').text() == "Terceiro" || $('#id_vinculo').val() == "Terceiro") { //se for terceiro
            $(".field-data_fim").show();
            $(".field-empresa").show();
            $('#id_data_fim').rules('add', { required: true });
            $('#id_empresa').rules('add', { required: true });
            $('#id_responsavel').rules('add', { required: true });
            $(".field-responsavel").show();
        } else {
            $(".field-data_fim").show();
            $(".field-responsavel").show();
            $('#id_data_fim').rules('add', { required: true });
            $('#id_responsavel').rules('add', { required: true });
        }
    }
}

$(document).ready(function () {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    // Validação do email
    $.validator.addMethod("email_inpe", function (value, element) {
        if (urlParams.get('motivo') != "atualizar")
            return true;
        else
            return this.optional(element) || /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@(inpe.br)$/.test(value);
    }, 'Forneça um email do inpe válido.');

    if (urlParams.get('motivo') == "externo") {
        $('#id_externo').prop('checked', true);
        $('#id_vinculo').find('[value=5]').remove();
        $('#id_vinculo').selectpicker('refresh');
        $(".field-ramal").hide();
        $(".field-predio").hide();
    } else { 
        $(".field-externo").hide();
    }

    $('#id_externo').on('change', function(){
        $('#id_externo').prop('checked', true);
    });
    
    //Validação do Formulário
    $("#_form").validate({
        rules: {
            first_name: { required: true, minlength: 3 },
            last_name: { required: true, minlength: 3 },
            email: { required: true, email_inpe: true },
            externo: { externo: true },
//J            telefone: { required: true, minlength: 8 },
//J            data_nascimento: { required: true }, rg: { required: true },
//J            cpf: { required: true },
            predio: { required: true },
            data_inicio: { required: true },
            vinculo: { required: true, min: 2 },
            ramal: { required: true },
            password: { required: true, minlength: 10, pwcheck: true, },
            confirm_password: { required: true, equalTo: "#id_password" },
        },
        messages: {
            confirm_password: "As senhas devem ser iguais",
            telefone: { minlength: "Por favor, forneça ao menos {0} caracteres.", },
            email: { email: "Forneça um email válido", },
            password: {
                pwcheck: "Forneça uma senha forte",
                minlength: "Por favor, forneça ao menos {0} caracteres.",
            }
        },
        errorElement: 'span',
        errorPlacement: function ( error, element ) {
            // Add the `help-block` class to the error element
            error.prependTo($(element).parents(".form-row-box").find('.form-row-error'));
        },
        highlight: function (element, errorClass, validClass) {
            $(element).addClass('is-invalid');
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass('is-invalid');
        },
        submitHandler: function (form) {
            neou_cms.remove_error_messages(); 
        },
    });
    // Esconde a data_fim se for servidor
    combo_vinculo()
    $("select#id_vinculo").change(function () {
        combo_vinculo()
    });

    // Deixar as mensagens do validate em portugues
    $.extend($.validator.messages, {
        required: "Campo obrigat&oacute;rio!",
    });

    //Mascaras
    $('#id_ramal').mask('0000');
//J    $('#id_cpf').mask('999.999.999-99');
//J    $('#id_data_nascimento').mask('99/99/9999');
    $('#id_data_inicio').mask('99/99/9999');
    $('#id_data_fim').mask('99/99/9999');
    
    var behavior = function (val) {
        return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
    },
    options = {
        onKeyPress: function (val, e, field, options) {
            field.mask(behavior.apply({}, arguments), options);
        }
    };
    
//J    $('#id_telefone').mask(behavior, options);
});




