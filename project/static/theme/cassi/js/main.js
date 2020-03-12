/* ===================================
--------------------------------------
	Cassi | Photo Studio HTML Template
	Version: 1.0
--------------------------------------
======================================*/


'use strict';

$(window).on('load', function() {
	/*------------------
		Preloder
	--------------------*/
	$(".loader").fadeOut();
	$("#preloder").delay(400).fadeOut("slow");

	/*------------------
		Masonry
	--------------------*/
	$('.gallery-gird').masonry();

});

(function($) {
	/*------------------
		Navigation
	--------------------*/
	$("#menu-canvas-show").on('click', function () {
		$('.offcanvas-menu-wrapper').fadeIn(400, function () {
			$('.offcanvas-menu-wrapper').addClass('active');
		}).css("display", "flex");
	});
	$("#menu-canvas-close").on('click', function () {
		$('.offcanvas-menu-wrapper').removeClass('active').delay(1100);
		$('.offcanvas-menu-wrapper').fadeOut(400);
	});
	

	/*------------------
		Background Set
	--------------------*/
	$('.set-bg').each(function() {
		var bg = $(this).data('setbg');
		$(this).css('background-image', 'url(' + bg + ')');
	});


	/*------------------
		Hero Item Size
	--------------------*/
	function heroItemSize () {
		if($(window).width() > 767) {
			var header_h = $('.header-section').innerHeight();
			var footer_h = $('.footer-section').innerHeight();
			var window_h = $(window).innerHeight();
			var hero_item_h = ((window_h) - (header_h + footer_h + 5));
			$('.hero-item').each(function() {
				$(this).height(hero_item_h);
			});
			
		}
	}
	if($(window).width() > 767) {
		heroItemSize ();
		$(window).resize(function(){
			heroItemSize ();
		});
	}

	/*------------------
		Hero Slider
	--------------------*/
	$('.hero-slider').owlCarousel({
		loop: true,
		nav: true,
		dots: false,
		navText:['<i class="arrow_left"></i>','<i class="arrow_right"></i>'],
		mouseDrag: false,
		animateOut: 'fadeOut',
		animateIn: 'fadeIn',
		items: 1,
		autoplay: true,
		smartSpeed: 1000,
	});

})(jQuery);

