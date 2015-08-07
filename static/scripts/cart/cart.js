$(function() {
    $('.quantity, .price, .delivery').keypress(function (e) {
        var code = e.keyCode ? e.keyCode : e.which;
        if (code<48 || code>57) e.preventDefault();
    });

    $('.quantity, .price, .delivery').change(function(){
        var quantity = $(this).val();
        var id= $(this).attr("rel");
        var shop_name = $(this).attr("rev");
        var prev=this;
        if (parseInt(quantity))
            $.getJSON("/change_number/"+id+"/"+quantity+"/", function(recv){
                if (recv=='error'){
                    alert('error')
                } else{
                    if (recv['max']){
                        show_message_error(gettext('Максимально доступное количество этого товара ')+recv['max'])
                        $(prev).val(recv['q']);
                    } else {
                    $("#shop_name_"+shop_name).html(recv['shop_price']);
                    $("#full_price_"+id).html(recv['price']);
                    $("#sum").html(recv['sum'])
                    }
                }

            });
    });

})
