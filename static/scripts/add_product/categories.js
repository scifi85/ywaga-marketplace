var nc = 0;
var category_line=new Array();
var write=true;

function get_categories(category,add){
    var arg='';

    for (var i=0; i<category.length;i++)
        arg+='<catend>'+encodeURIComponent(category[i])+"</catend>";

    $.getJSON("/shop/get_categories/"+arg+"/",
        function(recv){

            switch(recv){
                case 'finished':
                    $("#add_own_category").show();
                    if (add)
                        for (var i=nc; i<=initial_categories-1; i++){
                            $("#id_categories").append("<input maxlength='300' type=\"text\" value=\"\" id=\"category"+nc+"\" name=\"category"+nc+"\" rel=\""+nc+"\" class=\"category onlyStr\"><br>");
                            nc++;
                        }
                    break;
                case 'no category':
                    $("#add_own_category").show();
                    if (add)
                        for (var i=nc; i<=initial_categories-1; i++){
                            $("#id_categories").append("<input maxlength='300' type=\"text\" value=\"\" id=\"category"+nc+"\" name=\"category"+nc+"\" rel=\""+nc+"\" class=\"category onlyStr\"><br>");
                            nc++;
                        }
                    break;
                default:
                    $("#id_categories").append('<select id="category'+nc+'" rel="'+nc+'" class="category onlyStr" name="category'+nc+'"></select>');
                    for (var j=0;j<recv.length;j++)
                        $("#category"+nc).append('<option value="'+recv[j][1]+'">'+recv[j][0]+'</option>')
                    nc++;
            }
            return false;
        }

    );
    return false;
}

$(function() {

    $("#add_own_category").hide();
    $(".category").live('change', function(){
        if(this.type=="select-one"){
            var category=$(this,":selected").val();
            var id=parseInt($(this).attr("rel"));

            if (id<nc){
                for (var j=id+1;j<=nc;j++) $("#category"+j).remove();

                category_line.splice(id,nc-id);
                nc=id+1;
                write=false;
            }
            switch (category) {
                case 'Please choose a category':
                    $("#add_own_category").hide();
                    break;
                case 'Other':
                    if (category_line.length>=5)
                        $("#add_own_category").hide();
                    else
                        $("#add_own_category").show();
                    break;
                default:
                    category_line.push(category);
                    get_categories(category_line);
                    $("#add_own_category").hide();
            }
        }
    });
    $("#add_own_category").click(function(){
            $("#id_categories").append("<input maxlength='300' type=\"text\" id=\"category"+nc+"\" rel=\""+nc+"\"  name=\"category"+nc+"\" class=\"category onlyStr\"><br>");
            nc++;
        if (nc>=5)
            $("#add_own_category").hide()
        return false;
    })


});
