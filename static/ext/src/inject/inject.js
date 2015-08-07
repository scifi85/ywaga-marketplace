
chrome.extension.sendMessage({}, function(response) {
	var readyStateCheckInterval = setInterval(function() {
	if (document.readyState === "complete") {
		clearInterval(readyStateCheckInterval);

		// ----------------------------------------------------------
		// This part of the script triggers when page is done loading
		console.log("Hello. This message was sent from scripts/inject.js");
		// ----------------------------------------------------------
        $(function(){
            var url = document.URL;
            alert(url);
            url = encodeURIComponent(url);
            $('body').prepend('<a href="http://ywaga.com/shop/addProductFromTB/?link='+url+'" class="btn btn-info" target="_blank">ADD TO CART</a>')
        })

	}
	}, 10);
});
function f(){
    alert(2);
}
chrome.pageAction.onClicked.addListener(f);

