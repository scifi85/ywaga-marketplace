$(function() {
    if ($(".size").length==1)
        $(".size").attr('checked','on');
    if ($(".type").length==1)
        $(".type").attr('checked','on');
    if ($(".color").length==1)
        $(".color").attr('checked','on');
    $(".color, .size, .type").click(function(){
        var color = parseFloat($('[name=color]:checked').attr("rel"));
        var size = parseFloat($('[name=size]:checked').attr("rel"));
        var type = parseFloat($('[name=type]:checked').attr("rel"));

        if (!color) color = 0;
        if (!size) size = 0;
        if (!type) type = 0;
        var price =Math.max(color,size,type);
        if (price/parseInt(price)==1)
            price=price+'.0';
        $("#priceProduct").html(price+' грн.');
    })

    $("#buy").live('click',function(event){

        if ($('[name=color]:checked').val()==undefined && $(".color").length>0) {
            show_message_error(gettext('Укажите цвет'));
//            alert('Choose color');
            event.preventDefault();
            return false;
        }

        if ($('[name=size]:checked').val()==undefined && $(".size").length>0) {
            show_message_error(gettext('Укажите размер'));
//            alert('Choose size');
            event.preventDefault();
            return false;
        }
        if ($('[name=type]:checked').val()==undefined && $(".type").length>0) {
            show_message_error(gettext('Укажите тип'));
//            alert('Choose type');
            event.preventDefault();
            return false;
        }

    })
})
