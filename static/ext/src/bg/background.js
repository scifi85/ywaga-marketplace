// if you checked "fancy-settings" in extensionizr.com, uncomment this lines

// var settings = new Store("settings", {
//     "sample_setting": "This is how you use Store.js to remember values"
// });


//example of using a message handler from the inject scripts
chrome.extension.onMessage.addListener(
  function(request, sender, sendResponse) {
  	chrome.pageAction.show(sender.tab.id);
    sendResponse();



  });


if( ! localStorage['lang'])
{
    //Получаем язык, используемый в браузере
    var lang = chrome.i18n.getMessage("@@ui_locale");
    if (lang == 'ru')
        localStorage['lang'] = "ru";
    else
        localStorage['lang'] = "en";
}


function check(tab_id, data, tab){

    chrome.tabs.executeScript(tab.id, {file: "base.js"});


    var patt=/.*tmall.com|taobao.com.item\.htm.*id(=|%3D)\d+/.test(tab.url);
    var x=!(/.*xoposho\.com/.test(tab.url));
    if ((patt) && (x))
        chrome.pageAction.show(tab_id);

};
function add_to_card(Tab, tab){
//    alert(3);
    var answer = confirm (chrome.i18n.getMessage("AddToCart"));
    if(answer) {
        var google_trans=/translate.google.com/.test(Tab.url);
        var url;
        if (google_trans){
            url=/&u=(.*)/.exec(Tab.url)[1];
            url = decodeURIComponent(url);
        }
        else
            url=Tab.url;

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://ywaga.com/shop/addProductFromTB/",true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4){
                if (xhr.responseText=='error'||xhr.responseText=='') {
                    alert(chrome.i18n.getMessage("error"))
                } else {
                    alert(chrome.i18n.getMessage("ProductAdded"));
                    chrome.tabs.getAllInWindow(null, function(tabs){
                        chrome.tabs.create({"url":"http://ywaga.com/shop/edit_product/"+xhr.responseText+"/"});
                    });
                }
            }
        }
        xhr.send('link='+encodeURIComponent(url)+'&plugin=true&note=');
    }
};

chrome.tabs.onUpdated.addListener(check);
chrome.pageAction.onClicked.addListener(add_to_card);