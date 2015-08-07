$(function() {

    $(".btn-sc").click(function(event){

        //Product name validator (name_id)
        var name=$("#id_name").val();

//        if (name.length<3 || name[0]==' ')
//            event.preventDefault();

        $('#new_picture .prom_picture').each(function(i,v){
            var rel = $(v).find('.del_prom').attr('rel');
            if (rel){
                var el=$('<input type="hidden" name="mark_picture_'+rel+'" value="'+i+'">')
                $('#product_form').append(el)
            }
            var rev = $(v).attr('rev');
            if (rev){
                var el=$('<input type="hidden" name="mark_tmp_picture_'+rev+'" value="'+i+'">')
                $('#product_form').append(el)
            }
        });

        $('.uploaded-block .uploaded-block-small .thumbholder img').each(function(i,v){
            var rel = $(v).attr('rel');

            if (rel){

                var el=$('<input type="hidden" name="mark_front_picture_'+rel+'" value="'+i+'">');
                $('#product_form').append(el)
            }
            var rev = $(v).attr('rev');
            if (rev){
                var el=$('<input type="hidden" name="mark_tmp_front_picture_'+rev+'" value="'+i+'">')
                $('#product_form').append(el)
            }
        });

        var id=$(this).attr("id");

        if (id=='Save')
            $("#save_id").val("Save");
        if (id=='SaveContinue')
            $("#save_id").val("SaveContinue");
        if (id=='SaveNew')
            $("#save_id").val("SaveNew");

    });

});




