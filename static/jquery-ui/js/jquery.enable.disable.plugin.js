/* Copyright (c) 2010 José Joaquín Núñez (josejnv --at-- gmail punto com) http://joaquinnunez.cl/blog/
 * Licensed under GPL (http://www.opensource.org/licenses/gpl-2.0.php)
 * Use only for non-commercial usage.
 *
 * Version : 0.1
 *
 * Requires: jQuery 1.2+
 * 
 * select support added by Ajay Sawant ( ajay.sawant --at-- prosares punto com )  http://prosares.co.cc/
 *
 */
 
(function($)
{
  jQuery.fn.EnableDisable = function(options)
  {
    var defaults = {
      enabler: null,
      enablerVal: null,
      on_enable: function(){},
      on_disable: function(){}
    };

    var opts = $.extend(defaults, options); 

    this.each(function(){
      var field_to_be_enabled_or_disabled = this;

      // init
      var enable = false;
      jQuery(opts.enabler).each(function(){
        if(this.tagName == "INPUT")
        {
          if(jQuery(this).attr('checked'))
          {
            enable = true;
          }
        }
        else if(this.tagName == "SELECT" )
        {
          if(jQuery.inArray(jQuery(this).val(), opts.enablerVal) >= 0)
          {
            enable = true;
          }
        }
      });

      if(enable)
      {
        jQuery(field_to_be_enabled_or_disabled).removeAttr('disabled');
      }
      else
      {
        jQuery(field_to_be_enabled_or_disabled).attr('disabled','disabled');
      }

      // on click
      var radios = new Array();
      var selects = new Array();
      var checkboxs = new Array();

      jQuery(opts.enabler).each(function(){
        if(this.tagName == "INPUT" && this.type == "radio")
        {
          radios.push($(this).attr('name'));
        }
        else if(this.tagName == "INPUT" && this.type == "checkbox")
        {
        	checkboxs.push($(this).attr('id'));
        }
        else if(this.tagName == "SELECT")
        {
          selects.push($(this).attr('id'));
        }
      });

      radios = array_unique(radios);
      selects = array_unique(selects);
      checkboxs = array_unique(checkboxs);

      jQuery.each(radios, function(){
        jQuery('input[name='+this+']').click(function(){
          var this_field = this;
          var enable = false;
          jQuery(opts.enabler).each(function(){
            if( jQuery(this).attr('id') == jQuery(this_field).attr('id') && jQuery(this).attr('checked') )
            {
              enable = true;
            }
          });
          // enable or disable
          jQuery.enable_or_disable(field_to_be_enabled_or_disabled, enable, opts);
        });
      });

      jQuery.each(selects, function(){
        jQuery('#'+this).bind("change", function(){
          var this_field = this;
          var enable = false;
          jQuery(opts.enabler).each(function() {
            if(jQuery(this).attr('id') == jQuery(this_field).attr('id') && jQuery.inArray(jQuery(this).val(), opts.enablerVal) >= 0)
            {
              enable = true;
            }
          });
          // enable or disable
          jQuery.enable_or_disable(field_to_be_enabled_or_disabled, enable, opts);
        });
      });
      
      jQuery.each(checkboxs, function(){
        jQuery('#'+this).bind("change", function(){
          var this_field = this;
          var enable = false;
          jQuery(opts.enabler).each(function() {
            if( jQuery(this).attr('id') == jQuery(this_field).attr('id') && jQuery(this).attr('checked') )
            {
              enable = true;
            }
          });
          // enable or disable          
          jQuery.enable_or_disable(field_to_be_enabled_or_disabled, enable, opts);
        });
      });
      
      
    });
  }
})(jQuery);

/**
 * this function was taken from http://www.forosdelweb.com/f13/array_unique-javascript-215906/#post732378
 */

function array_unique(arr)
{
  if (arr.length>1)
  {
    var arr=arr.sort();
    var arrUnique=new Array(arr[0]);
    for (i=1;i<arr.length;i++)
    {
      if(arr[i]!=arrUnique[arrUnique.length-1])
      {
        arrUnique.push(arr[i]);
      }
    }
    return arrUnique;
  }
  else
  {
    return arr;
  }
}

jQuery.enable_or_disable = function (field_to_be_enabled_or_disabled, enable, opts)
{
  if (enable)
  {
    jQuery(field_to_be_enabled_or_disabled).removeAttr('disabled');
    opts.on_enable();
  }
  else
  {
    jQuery(field_to_be_enabled_or_disabled).attr('disabled', 'disabled');
    opts.on_disable();
  }
};