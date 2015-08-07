$(function() {
    $('.quantity, .price, .delivery').keypress(function (e) {

        var code = e.keyCode ? e.keyCode : e.which;

        if (!(code>48 || code<57 || code==46)) e.preventDefault();
    });
    $('.quantity, .price, .delivery').change(function(){

        var type= $(this).attr("class");
        var value = $(this).val();
        var id= $(this).attr("rel");
        loaderShow();
            $.getJSON("/shop/change/"+id+"/"+value+"/"+type+'/', function(recv){
                loaderHide();
                if (recv!='error'){
                    $("#full_price_"+id).html(recv['price']);
                    $("#order_price_"+recv['order_id']).html(recv['order_price'])
                    show_message_info(gettext('Изменения сохранены'))
                } else
                    show_message_error('Ошибка')
            });
    });
    $('.track_code').click(function(){
        var track = $(this).prev().val();
        var order= $(this).attr("order");
        loaderShow();
        $.getJSON("/shop/upload_track_code/"+order+"/"+encodeURI(track)+"/", function(recv){
            loaderHide();
            if (recv=='ok')
                show_message_success(gettext('Трекинг код отослан'))
            else
                show_message_error(gettext('Ошибка'));
        });

    })
});
