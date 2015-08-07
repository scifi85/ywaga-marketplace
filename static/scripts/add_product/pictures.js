var z=1;
var y=1;
$(function() {
    $("#add_pic").click(function(){
        //open add picture from hard drive window
        $("#front_"+z).click();
        return false;
    });
    $("#add_pic2").click(function(){
        //open add picture from hard drive window
        $("#promo_pic_"+y).click();
        return false;
    });


    $("#show_webcam, #show_webcam2").click(function(){
        //Show webcamera dialog
        $('#modal-camera').modal('show');
        document.getElementById('upload_results').innerHTML = '';
        $("#webcam").html();

        //Initialize webcamera
        webcam.set_api_url( '/shop/capture_tmp/' );
        webcam.set_quality( 100 );
        webcam.set_shutter_sound( true );
        var wc= webcam.get_html(640, 480);
        $("#webcam").html(wc);
        if ($(this).attr('id')=='show_webcam')
            webcam.set_hook( 'onComplete', 'handle_webcam_pic' );
        if ($(this).attr('id')=='show_webcam2')
            webcam.set_hook( 'onComplete', 'handle_webcam_pic2' );

    });
});

function add_image_from_computer(input){

    var ext = $(input).val().split('.').pop().toLowerCase();
    if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1){
        input.value='';
        show_message_error(gettext('Вы можете добавить только фотографии'));
        return false;
    }
    if (input.files[0].size>=2000000){
        input.value='';
        show_message_error(gettext('Максимальный размер файла 2MB'));
        return false;
    }
    loaderShow();
    //add picture from hard drive
    if (input.files && input.files[0]) {
        if (typeof FileReader == "undefined")
            $.ajaxFileUpload({
                url:'/shop/capture_tmp/',fileElementId:input.id,
                success: function (data, status) {
                           var msg =data.body.innerText;
                        var el= $('<div class="uploaded-block-small" >'+
                                    '<div class="linkholder">'+
                                        '<div class="arrows">'+
                                            '<div class="arrow-up">'+
                                                '<a href="#">&#9650;</a>'+
                                            '</div>'+
                                        '<div class="arrow-down">'+
                                            '<a href="#">&#9660;</a>'+
                                        '</div>'+
                                    '</div>'+
                                    '<div class="delete-thumbs">'+
                                        '<a href="#" rev="'+z+'">&#10006;</a>'+
                                    '</div>'+
                                    '</div>'+
                                    '<div class="thumbholder">'+
                                        '<img src="" alt="" rev="'+z+'">'+
                                    '</div>'+
                                  '</div>');
                    $(el).find('img').attr('src','/media/'+msg);
                    $(el).appendTo('.uploaded-block');
                    changeSlider();

                    $('#product_form').append('<input type="hidden" id="front_pic_'+z+'" name="frontPic_'+z+'" value="'+msg+'">');
                    z++;
                    el='<input name = "front_'+z+'" id="front_'+z+'" type="file" class="input-file" style="visibility:hidden" onchange="add_image_from_computer(this);">'
                    $(el).appendTo('.add-pich2');
                    showNext();
                            }
            })
    if (typeof FileReader !== "undefined"){
        var reader = new FileReader();
            reader.onload = function (e) {
                var el= $('<div class="uploaded-block-small" rev="'+z+'">'+
                            '<div class="linkholder">'+
                                '<div class="arrows">'+
                                    '<div class="arrow-up">'+
                                        '<a href="#">&#9650;</a>'+
                                    '</div>'+
                                    '<div class="arrow-down">'+
                                        '<a href="#">&#9660;</a>'+
                                    '</div>'+
                                '</div>'+
                                '<div class="delete-thumbs">'+
                                    '<a href="#" rev="'+z+'">&#10006;</a>'+
                                '</div>'+
                            '</div>'+
                            '<div class="thumbholder">'+
                                '<img src="/media/photos/prod1_small.jpg" alt="" rev="'+z+'">'+
                                '</div>'+
                          '</div>')
                $(el).find('img').attr('src',e.target.result);
                $(el).appendTo('.uploaded-block');
                changeSlider();
                z++;
                el='<input name = "front_'+z+'" id="front_'+z+'" type="file" class="input-file" style="visibility:hidden" onchange="add_image_from_computer(this);">'
                $(el).appendTo('.add-pich2');
                showNext();
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    loaderHide();
}
function add_image_from_computer2(input){

    var ext = $(input).val().split('.').pop().toLowerCase();
    if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1){
        input.value='';
        show_message_error(gettext('Вы можете добавить только фотографии'));
        return false;
    }
    if (input.files[0].size>=2000000){
        input.value='';
        show_message_error(gettext('Максимальный размер файла 2MB'));
        return false;
    }
    loaderShow();
    if (typeof FileReader == "undefined")
    $.ajaxFileUpload({
        url:'/shop/capture_tmp/',fileElementId:input.id,
        success: function (data, status) {
            var msg =data.body.innerText;
            var el= $('<div class="prom_picture" rev="'+y+'">' +
                '<img src="" alt="">'+
                '<a href="#" class="del_prom" rev="'+y+'">&#10006;</a>' +
                '       </div>')

            $(el).find('img').attr('src','/media/'+msg);
            $('#new_picture').append(el);

            $('#product_form').append('<input type="hidden" id="promo_pic_'+y+'"name="promo_pic_'+y+'" value="'+msg+'">');
            y++;

            el='<input name = "prom_'+y+'" id="promo_pic_'+y+'" type="file" class="input-file" style="visibility:hidden" onchange="add_image_from_computer2(this);">'
            $('#product_form').append(el);
        }
    })
    if (typeof FileReader !== "undefined"){
    //add picture from hard drive
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var el= $('<div class="prom_picture" rev="'+y+'">' +
                        '<img src="" alt="">'+
                        '<a href="#" class="del_prom" rev="'+y+'">&#10006;</a>' +
                      '</div>')
            $(el).find('img').attr('src',e.target.result);
            $('#new_picture').append(el);
            y++;
            el='<input name = "prom_'+y+'" id="promo_pic_'+y+'" type="file" class="input-file" style="visibility:hidden" onchange="add_image_from_computer2(this);">'
            $('#product_form').append(el);
        }
        reader.readAsDataURL(input.files[0]);
    }
    }
    loaderHide();
}
function take_snapshot() {
    //make picture from web camera

    loaderShow();
    webcam.snap();
//    document.getElementById('upload_results').innerHTML = '<h1>Uploading...</h1>';
}
function handle_webcam_pic(msg) {
        //add picture from webcamera
//        $( "#box_camera" ).dialog( "close" );$( "#box_camera" ).remove();

    loaderHide();
    $('#modal-camera').modal('hide');

        var el= $('<div class="uploaded-block-small" >'+
                            '<div class="linkholder">'+
                                '<div class="arrows">'+
                                    '<div class="arrow-up">'+
                                        '<a href="#">&#9650;</a>'+
                                    '</div>'+
                                    '<div class="arrow-down">'+
                                        '<a href="#">&#9660;</a>'+
                                    '</div>'+
                                '</div>'+
                                '<div class="delete-thumbs">'+
                                    '<a href="#" rev="'+z+'">&#10006;</a>'+
                                '</div>'+
                            '</div>'+
                            '<div class="thumbholder">'+
                                '<img src="" alt="" rev="'+z+'">'+
                                '</div>'+
                            '</div>');


        $(el).find('img').attr('src','/media/'+msg);
        $(el).appendTo('.uploaded-block');
        changeSlider();

        $('#product_form').append('<input type="hidden" id="front_pic_'+z+'" name="frontPic_'+z+'" value="'+msg+'">');
        z++;
//        el='<input name = "front_'+z+'" id="front_pic_'+z+'" type="file" class="input-file" style="visibility:hidden" onchange="add_image_from_computer2(this);">'
        el='<input name = "front_'+z+'" id="front_'+z+'" type="file" class="input-file" style="visibility:hidden" onchange="add_image_from_computer(this);">'
        $('#product_form').append(el)

        show_message(gettext('Загрузка завершена!'));
        showNext();
        return false;
}

function handle_webcam_pic2(msg) {
    //add picture from webcamera
//    $( "#box_camera" ).dialog( "close" );$( "#box_camera" ).remove();
    loaderHide();
    $('#modal-camera').modal('hide');

    var el= $('<div class="prom_picture" rev="'+y+'">' +
                '<img src="" alt="">'+
                    '<a href="#" class="del_prom" rev="'+y+'">&#10006;</a>' +
        '       </div>')

    $(el).find('img').attr('src','/media/'+msg);
    $('#new_picture').append(el);

    $('#product_form').append('<input type="hidden" id="promo_pic_'+y+'"name="promo_pic_'+y+'" value="'+msg+'">');
    y++;
    el='<input name = "prom_'+y+'" id="promo_pic_'+y+'" type="file" class="input-file" style="visibility:hidden" onchange="add_image_from_computer2(this);">'
    $('#product_form').append(el);
    show_message(gettext('Загрузка завершена!'));

    return false;
}

