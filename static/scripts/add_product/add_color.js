//var colors =0;
//var sizes=0;
//var types =0;
function add_size(size,price){
    if (!price)
        var price = $("#id_price").val();
    var Size=$("<select  name='sizes_"+size+"'>"+
            "<option value=''>"+gettext('Пожалуйста выберите размер')+"</option>"+
            "<option value='XXXL'>XXXL</option>"+
            "<option value='XXL'>XXL</option>"+
            "<option value='XL'>XL</option>"+
            "<option value='L'>L</option>"+
            "<option value='M'>M</option>"+
            "<option value='S'>S</option>"+
            "<option value='XS'>XS</option>"+
            "<option value='XXS'>XXS</option>"+
            "<option value='XXXS'>XXXS</option>"+
        "</select>"+
        "<input class='onlyFloat' maxlength='6' type='text' id='id_size_price_"+size+"' name='size_price_"+size+"' placeholder='"+gettext('Цена')+"' value='"+price+"'>"+
        "<a href='#' class='delete'>"+gettext('Удалить')+"</a>");
    return Size;
}
function add_type(type,price){
    if (!price)
        var price = $("#id_price").val();
        var Type=$("<input type='text' maxlength='20' name='types_"+type+"'>"+
        "<input maxlength='8' class='onlyFloat' type='text' id='id_type_price_"+type+"' name='type_price_"+type+"' placeholder='"+gettext('Цена')+"' value='"+price+"'>"+
        "<a href='#' class='delete'>"+gettext('Удалить')+"</a>");

    return Type;
}
$(function() {
    var colors =$('.colors').length;
    var sizes=$('.sizes').length;
    var types =$('.types').length;
    if (colors>=9)
        $("#add_color").attr('class','btn disabled');
    if (sizes>=9)
        $("#add_size").attr('class','btn disabled');
    if (types>=9)
        $("#add_type").attr('class','btn disabled');
    $("#add_color").click(function(){
        if (colors<=9){
            $("#id_colors").append(add_color(colors));
            colors++;
        }
        if (colors>=9)
            $(this).attr('class','btn disabled');

    })
    $("#add_size").click(function(){
        if (sizes<=9){
            $("#id_sizes").append(add_size(sizes));
            sizes++;
        }
        if (sizes>=9)
            $(this).attr('class','btn disabled');
    })
    $("#add_type").click(function(){
        if (types<=9){
            $("#id_types").append(add_type(types));
            types++;
        }
        if (types>=9)
            $(this).attr('class','btn disabled');
    })
    $('.delete').live('click',function(){
        if ($(this).parent().attr('id')=='id_colors'){
            colors-=1;
            $("#add_color").attr('class','btn');
        }
        if ($(this).parent().attr('id')=='id_sizes'){
            sizes-=1;
            $("#add_size").attr('class','btn');
        }
        if ($(this).parent().attr('id')=='id_types'){
            types-=1;
            $("#add_type").attr('class','btn');
        }
        $(this).prev().prev().attr("value", "");
        $(this).hide();
        $(this).prev().hide();
        $(this).prev().prev().hide();
        return false;
    })

});
