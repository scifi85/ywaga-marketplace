function changeSlider(){
    $('.arrow-up, .arrow-down').each(function(i,v){
        $(v).removeClass('not-active')
    })
    $('.uploaded-block').children().first().find('.arrow-up').addClass('not-active');
    $('.uploaded-block').children().last().find('.arrow-down').addClass('not-active');

    var images =[];
    $('.uploaded-block img').each(function(i,v){
        images.push(v.src);
    })
//    alert(images.length);

    var saved_images = $('#slider-main img').length;
    var l=0;
    if (saved_images<images.length)
        var l = images.length-saved_images;

    for (i=1;i<=l+1;i++) {
        $('#slider-main').append('<img src="" alt="">');
        $('#slider-thumbs').append('<li rel="'+(i+saved_images)+'"><img src=""></li>');
    }


    $('#slider-main img').each(function(i,v){
        if (i<=images.length-1)
            v.src=images[i]
        else
            $(v).remove();

    })
    $('#slider-thumbs img').each(function(i,v){
        if (i<=images.length-1)
            v.src=images[i]
        else
            $(v).parent().remove();
    })

}

$(function(){
    changeSlider();
    $('.arrow-up a').live('click',function(){
        var clas =  $(this).parent().attr('class');
        if (/not-active/.test(clas))
            return false;
        var current = $(this).parent().parent().parent().parent();
        var pre = $(current).prev();

        var tmp=$(pre).html();
        $(pre).html(current.html());
        $(current).html(tmp);


        changeSlider();
        return false;
    })

    $('.arrow-down a').live('click',function(){
        var clas =  $(this).parent().attr('class');
        if (/not-active/.test(clas))
            return false;

        var current = $(this).parent().parent().parent().parent();
        var nex = $(current).next();

        var tmp=$(nex).html();
        $(nex).html(current.html());
        $(current).html(tmp);

        changeSlider();
        return false;
    })
    $('.delete-thumbs a').live('click',function(){
        $(this).closest('.linkholder').parent().remove();
        var id=$(this).attr('rel');

        if (id)
            $('#product_form').append('<input type="hidden" name="deleteFrontPicture'+id+'" value="'+id+'">')
        else {
            var id = $(this).attr('rev');
            $('#front_pic_'+id).remove();
        }

        changeSlider();
        return false;

    });
    $('.del_prom').live('click',function(){
        $(this).closest('.prom_picture').remove();
        var id=$(this).attr('rel');
        if (id)
            $('#product_form').append('<input type="hidden" name="deletePromoPic'+id+'" value="'+id+'">')
       else {
                var id = $(this).attr('rev');
                $('#promo_pic_'+id).remove();
            }

        return false;
    })

})
