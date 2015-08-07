function show_message(message){
    $("#info_text_message").html(message);
    $('#modal-info').modal('show');
    setTimeout(function(){
        $('#modal-info').modal('hide');
    }, 4000);
}
function show_message_info(message){
    $("#info_text_message").html(message);
    $('#modal-info').modal('show');
    setTimeout(function(){
        $('#modal-info').modal('hide');
    }, 4000);
}
function show_message_error(message){
    $("#danger_text_message").html(message);
    $('#modal-danger').modal('show');
}

function show_message_success(message){
    $("#success_text_message").html(message);
    $('#modal-success').modal('show');
    setTimeout(function(){
        $('#modal-success').modal('hide');
    }, 4000);
}
function loaderShow(){
    $('#modal-loader').modal({'show':true,'backdrop' :'static'});
}
function loaderHide(){
    $('#modal-loader').modal('hide');
}
$(function() {

    $('.confirm').click(function(e){
        if (this.localName=='a'){
            var message=$(this).attr('rel');
            $('#confirm_text_message').text(message);
            $('#modal-text').modal('show');
            var link=$(this).attr('href');
            var header = $(this).attr('rev');

            if (typeof header !== 'undefined' && header !== false)
                $('#confirm_text_header').text(header);


            $('#da').attr('href',link);
            $('#da').live('click',function(){
                $('#da').addClass('disabled');
            });
            e.preventDefault();
        }

    })
    $('.confirm').submit(function(e){
        if ((this.localName=='form')&&($(this).attr('rev')!='used')){
            var message=$(this).attr('rel');
            $('#confirm_text_message').text(message);
            $('#modal-text').modal('show');
            var prev=this;


            $('#confirm_text_header').text('Ywaga.com');
            $('#da').live('click',function(){
                if($('.confirm').attr('rev')!='used'){
                    $(prev).attr('rev','used');
                    $(prev).submit();
                    $('#da').addClass('disabled');
                }
            });
            e.preventDefault();
        }
    })
    $('.inputFieldConfirm').click(function(e) {
        $('#modal-inputform').modal('show');
        e.preventDefault();
        var message = $(this).attr('rel'),
        header = $(this).attr('rev');
        var href =$(this).attr('href');
        $('#input_form').attr('action',href);
        if (typeof header !== 'undefined' && header !== false)
            $('#confirm-input-header').text(header)
        else
            $('#confirm-input-header').text('YWAGA.com');

        if (typeof message !== 'undefined' && message !== false)
            $('#confirm-input-message').text(message)
        else
            $('#confirm-input-message').text('');

        $("#textFieldModal").keyup(function(){
            if ($(this).val()=='')
                $("#daInputForm").addClass("disabled")
            else
                $("#daInputForm").removeClass("disabled");
        })
        $("#daInputForm").live('click',function(e){

            if ($('#daInputForm').hasClass('disabled'))
                return false;
            if ($('#textFieldModal').val()==''){
                show_message_error(gettext('Поле не заполнено'));
                return false;
            }
            $('#modal-inputform').modal('hide');
            loaderShow();
            $('#input_form').submit();
        })
    })

})