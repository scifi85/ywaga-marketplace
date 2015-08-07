$(function() {
    //Handle promotion
    //On the start
    $("#id_promotion_price").hide();
    var is_promotion=$('#id_is_promotion').is(':checked');
    if (is_promotion) $("#id_promotion_price").show();
    //On change
    $("#id_is_promotion").change(function(){
        var is_promotion=$('#id_is_promotion').is(':checked');
        if (is_promotion)
            $("#id_promotion_price").show();
        else
            $("#id_promotion_price").hide();
    })

    //Handle preorder
    //On the start
    $("#id_preorder_days").hide();
    var preorder=$('#id_preorder').is(':checked');
    if (preorder) $("#id_preorder_days").show();
    //On change
    $("#id_preorder").change(function(){
        var preorder=$('#id_preorder').is(':checked');
        if (preorder)
            $("#id_preorder_days").show();
        else
            $("#id_preorder_days").hide();
    })

    //Handle external
    //On the start
    
    //On change
    $("#id_is_external").change(function(){
        var external = $('#id_is_external').is(':checked'),
            delivery= $('#id_external_delivery'),
            free = $('.freelabel');
        if (external) {
            delivery.hide();
            free.show();
        } else {
            delivery.show();
            free.hide();
        }
    });
    $("#id_is_external").change();

//    var barcode=1;
//    $("#plus_barcode").click(function(){
//        //add new barcode
//        barcode++;
//        $(".add_barcode").last().append(""+
//            "<div class=\"control-group add-product add_barcode\">"+
//            "<input type=\"text\" class=\"input-xlarge\" name=\"new_barcode"+barcode+"\" placeholder=\"Barcode  \">" +
//            "<i class=\"icon-barcode\"></i></div>");
//    });
    var barcode=$('.barcodes').length;

    $("#plus_barcode").click(function(){
        //add new barcode
        if (barcode<=4){
            barcode++;
            $(".add_barcode").last().append(""+
                "<div class=\"control-group add-product add_barcode\">"+
                "<input maxlength='255' type=\"text\" class=\"input-xlarge\" name=\"new_barcode"+barcode+"\" placeholder=\""+gettext('Артикул')+"\">" +
                "<a href='#' class='delete_barcode'>"+gettext('Удалить')+"</a>"+
                "</div>");
        }
        if (barcode>=4)
            $(this).attr('class','btn disabled')
    });
    $('.delete_barcode').live('click',function(){
        barcode--;
        $("#plus_barcode").attr('class','btn');
        $(this).prev().val('');
        $(this).prev().hide();
        $(this).hide();
        return false;
    })

    var keyword=$('.keywords').length;

    $("#plus_keyword").click(function(){
        //add new barcode
        if (keyword<=4){
            keyword++;
            $(".add_keyword").last().append(""+
                "<div class=\"control-group add-product add_keyword\">"+
                "<input maxlength='255' type=\"text\" class=\"input-xlarge\" name=\"new_keyword"+keyword+"\" placeholder=\""+gettext('Ключевое слово')+"\">" +
                "<a href='#' class='delete_keyword'>"+gettext('Удалить')+"</a>"+
                "</div>");
        }
        if (keyword>=4)
            $(this).attr('class','btn disabled')
    });
    $('.delete_keyword').live('click',function(){
        keyword--;
        $("#plus_keyword").attr('class','btn');
        $(this).prev().val('');
        $(this).prev().hide();
        $(this).hide();
        return false;
    })
});
