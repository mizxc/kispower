(function ($) {
  "use strict";
  // menu fixed js code
  $(window).scroll(function () {
    var window_top = $(window).scrollTop() + 1;
    if (window_top > 50) {
      $('.main_menu').addClass('menu_fixed animated fadeInDown');
    } else {
      $('.main_menu').removeClass('menu_fixed animated fadeInDown');
    }
  });
  
  if (document.getElementById('default-select')) {
		$('select').niceSelect();
  }
  
}(jQuery));