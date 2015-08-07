//
//function add_base(base_name){
//    window.location.href="/shop/add_new_base/" + base_name+'/'
//}
//
//function edit_base(new_name,old_name){
//    window.location.href="/shop/change_base_name/" + old_name+'/'+new_name+'/';
//}
//
//$(function() {
//    $(".addnew-base").click(function(){
//        input_window("Add new base name",add_base);
//    });
//    $(".edit-base").click(function(){
//        var old_name=$(this).attr("rel");
//        input_window("Enter new base name",edit_base,old_name);
//    })
//    $(".delete-base,.delete_product").click(function(e){
//        confirmation_window("Delete ?",e);
//    });
//
//

//})

$('html').ajaxSend(function(event, xhr, settings) {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.

        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

$(function() {
    $('input[type=file]').change(function(){
        if (this.files[0].size>=2000000){
            this.value='';
            show_message_error(gettext('Максимальный размер файла 2MB'));
            return false;
        }
    })
    $('.disabled').live('click', function(e) {
        e.preventDefault();
    })
    $('.onlyStr').live('keydown',function(e){
        var code = (e.keyCode ? e.keyCode : e.which);
        if (code==8 || code==9)
            return true;
        if (code>=48 && code<=57)
            e.preventDefault();
    })
    $('.onlyInt').live('keydown',function(e){
        var code = (e.keyCode ? e.keyCode : e.which);

        if (code==8 || code==9)
            return true;
        if ((code<48 || code>57 ) && (code<96 || code>105))
            e.preventDefault();
    })
    $('.onlyFloat').live('keydown',function(e){
        var code = (e.keyCode ? e.keyCode : e.which);
        if (code==8 || code==190 || code==9)
            return true;
        if ((code<48 || code>57 ) && (code<96 || code>105))
            e.preventDefault();
    })
    $('.trust').attr('title',gettext('Доверенный продавец'));

})