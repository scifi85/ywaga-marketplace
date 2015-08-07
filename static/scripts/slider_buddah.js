var currentImage; 
var currentIndex = -1; 
var interval; 
function showImage(index){ 
	if(index < $('#slider-main img').length){ 
	var indexImage = $('#slider-main img')[index] 
	if(currentImage){ if(currentImage != indexImage ){
	 	$(currentImage).css('z-index',2); 
	 	clearTimeout(myTimer); 
	 	$(currentImage).fadeOut(300, function() {
	  	myTimer = setTimeout("showNext()", 5000); 
	  	$(this).css({'display':'none','z-index':1})
	   	}); 
	   	} 
	   	} 
	   	$(indexImage).css({'display':'block', 'opacity':1});
	   	currentImage = indexImage; 
	   	currentIndex = index; 
	   	$('#slider-thumbs li').removeClass('active'); 
	   	$($('#slider-thumbs li')[index]).addClass('active'); 
	   } 
} 
    
function showNext(){ 
  	var len = $('#slider-main img').length; 
    var next = currentIndex < (len-1) ? currentIndex + 1 : 0; 
    showImage(next); 
}   
var myTimer;  
    $(document).ready(function() {
      	myTimer = setTimeout("showNext()", 5000);
       	showNext(); 
       //Load first image 
       $('#slider-thumbs li').live('click',function(e){
        	var count = $(this).attr('rel'); 
        	showImage(parseInt(count)-1);
        });
});

