$(document).ready(function(){
	var rated = 0;
	$(window).scroll(function(){
		positionScroll();
	});

	$('.user-rating .rating-dynamic span').click(function(){
		total = $('.user-rating .rating-dynamic span').length;
		voto  = $(this).index();

		var parametros = {
			'id_dir' : $('#id_dir').val(),
			'value' : total - voto
        };
        if(rated == 0) {
			$.ajax({
				url: "/set_rate/",
				type: "post",
				data: parametros,
				success: function(request){
					for (i=5; i>=voto;i--) {
						$('.user-rating .rating-dynamic span:eq('+i+')').addClass('rating');
					}
					$('.awe-star').css({'cursor': 'none'});
					$('.user-rating .value').html(request+'/'+total);
					rated = 1
				},
				error:function(){
				}
			});
		}
	});
	
	/*$.ajax({
		url:"/whois_get/ajax/",
		success: function(msg){
			if(msg == 0){
				whois();
			}
		}
	});*/

	$('#whois .close').click(function(){
		$('#whois').css({'display':'none', 'z-index':'1000'});
		$('#whois').removeClass('in');
		$('#bg_whois').css({'height':$(document).height() + 500, 'display':'none'});
		$('body').css({'overflow':'auto'});
	});

	$('#whois_form').submit(function(e){
		$.ajax({
			type:"POST",
			url:"/whois_set/ajax/",
			data:$('#whois_form').serialize(),
			success: function(msg){
				location.reload();
				if(msg == 'ok')
				{
					$('#whois').removeClass('in');
					$('#bg_whois').hide();
					$('body').css({'overflow':'auto'});
				}
				/*var msg = msg.split('|')
				if(msg[0] == 'ok'){
					window.location = '/?' + Math.floor(Math.random() * 51) + 25;
				}else{
					$('.message').html('<span class="mg_error">' + msg[1] + '</span>'); setTimeout(function(){
						$('.message').html('');
					}, 3500);
					$('#password').val('');
				}*/
			}
		});
		e.preventDefault();
	});

	$('#login_form').submit(function(e){
		$.ajax({
			type:"POST",
			url:"/accounts/login/ajax/",
			data:$('#login_form').serialize(),
			success: function(msg){
				var msg = msg.split('|')
				if(msg[0] == 'ok'){
					window.location = '/accounts/dashboard/';
					//window.location = '/?' + Math.floor(Math.random() * 51) + 25;
				}else{
					$('.message').html('<span class="mg_error">' + msg[1] + '</span>'); setTimeout(function(){
						$('.message').html('');
					}, 3500);
					$('#password').val('');
				}
			}
		});
		e.preventDefault();
	});

	$('#forgot_form').submit(function(e){
		$.ajax({
			type:"POST",
			url:"/accounts/forgot/ajax/",
			data:$('#forgot_form').serialize(),
			success: function(msg){
				var msg = msg.split('|')
				if(msg[0] == 'ok'){
					$('.message').html('<span class="mg_ok">' + msg[1] + '</span>'); setTimeout(function(){
						$('.message').html('');
						$('#signInModal #forgot').hide();
						$('#signInModal #login').show();
					}, 4000);
					$('#forgot_email').val('');
				}else{
					$('.message').html('<span class="mg_error">' + msg[1] + '</span>'); setTimeout(function(){
						$('.message').html('');
					}, 2800);
					$('#forgot_email').val('');
				}
			}
		});
		e.preventDefault();
	});

	$('#btn_guardar').click(function(e){
		if($('#score').val().match(/^\d+(?:\.\d{2})$/)){
			$.ajax({
				type:"POST",
				url:$('#setComplete').attr('data-url'),
				data:$('#data_reservation').serialize(),
				success: function(msg){
					location.reload();
				}
			});
		}else{
			$('.msg_reservation').html('Error: Compruebe el formato para el "Total de la Cuenta".')
			setTimeout(function(){
				$('.msg_reservation').html('');
			}, 5000)
		}
		e.preventDefault();
	});
	

	$('#btn_forgot').click(function(){
		$('#signInModal #login').hide();
		$('#signInModal #forgot').show();
		$('#email').val('');
		$('#password').val('');
	});

	$('#btn_back').click(function(){
		$('#signInModal #forgot').hide();
		$('#signInModal #login').show();
		$('#forgot_email').val('');
		return false;
	});

	$('.collapse').live('show', function(){
	    $(this).parent().find('a .icon').attr('class', 'icon ent-minus'); //add active state to button on open
	});

	$('.collapse').live('hide', function(){
	    $(this).parent().find('a .icon').attr('class', 'icon ent-plus'); //remove active state to button on close
	});

	// carousel demo
    $('#carouselslide').carousel()

	//========================== SlideJS Slider Initiation ============================// 

	/*
	var triangle = "<div class='triangle'></div>";
	var block = "<div class='block'></div>";
	*/

	var slider = $('#slidejs'),
	 	sliderCaption = $('#bon-slider-caption');

	if (slider.size() > 0) {
		slider.slides({
			preload: true,
			preloadImage: 'img/assets/ajax-loader.gif',
			play: 5000,
			pause: 2500,
			hoverPause: true,
			generateNextPrev: true,
			pagination: true,
			next: 'slide-next',
			prev: 'slide-prev',
			generatePagination: true,
			autoHeight: false,
			effect: 'fade',
			crossfade: true,
			paginationClass : 'slides-paginate',
			container: 'slides-container',
	        slidesLoaded: function() {
	            slider.find('.slides-paginate').addClass('visible-desktop');

	        }
		});
	}
	slider.find('.slide-next').append('<span class="awe-chevron-right"></span>');
    slider.find('.slide-prev').append('<span class="awe-chevron-left"></span>');
    /*
    if(slider.find('.slide-outer').children('.triangle').size() < 1){
		$('.slide-outer').prepend(triangle);
	}
	if(slider.find('.slide-outer').children('.block').size() < 1) {
		$('.slide-outer').prepend(block);
	}
	*/
	

	//========================== Camera Slider Initiation ============================// 

	var slider2 = $('#cameraslide');

	if(slider2.size() > 0) {
		slider2.camera({
			thumbnails: false,
			height: '376px',
			playPause: false
		});
	}
	/*
	if (slider2.find('.camera_overlayer').children('.triangle').size() > 0) {
		$('.camera_overlayer').remove('.triangle');
	}
	else {
		$('.camera_overlayer').prepend(triangle);
	}
	if (slider2.find('.camera_overlayer').children('.block').size() > 0) {
		$('.camera_overlayer').remove('.block');
	}
	else {
		$('.camera_overlayer').prepend(block);
	}
	*/
	if (slider2.find('.camera_next').children('span').not('.awe-chevron-right')) {
		$('.camera_next').children().addClass('awe-chevron-right');
	}
	if (slider2.find('.camera_prev').children('span').not('.awe-chevron-left')) {
		$('.camera_prev').children().addClass('awe-chevron-left');
	}
	if (slider2.find('.camera_play').children('.ent-play').size() < 1 ) {
		$('.camera_play').append('<span class="ent-play"></span>');
	}
	if (slider2.find('.camera_stop').children('.ent-pause').size() < 1 ) {
		$('.camera_stop').append('<span class="ent-pause"></span>');
	}

	//========================== Adding Pagination to Carousel ============================//

	$('.carousel[id]').each(
		function() {
			var html = '<div class="carousel-nav" data-target="' + $(this).attr('id') + '"><ul>';
			
			for(var i = 0; i < $(this).find('.item').size(); i ++) {
				html += '<li><a';
				if(i == 0) {
					html += ' class="active"';
				}
				
				html += ' href="#">•</a></li>';
			}
			
			html += '</ul></li>';
			$(this).before(html);
			//$('.carousel-control.left[href="#' + $(this).attr('id') + '"]').hide();
		}
	).bind('slid',
		function(e) {
			var nav = $('.carousel-nav[data-target="' + $(this).attr('id') + '"] ul');
			var index = $(this).find('.item.active').index();
			var item = nav.find('li').get(index);
			
			nav.find('li a.active').removeClass('active');
			$(item).find('a').addClass('active');
			
			/*if(index == 0) {
				$('.carousel-control.left[href="#' + $(this).attr('id') + '"]').fadeOut();
			} else {
				$('.carousel-control.left[href="#' + $(this).attr('id') + '"]').fadeIn();
			}
			
			if(index == nav.find('li').size() - 1) {
				$('.carousel-control.right[href="#' + $(this).attr('id') + '"]').fadeOut();
			} else {
				$('.carousel-control.right[href="#' + $(this).attr('id') + '"]').fadeIn();
			}
			*/
		}
	);
	
	$('.carousel-nav a').bind('click',
		function(e) {
			var index = $(this).parent().index();
			var carousel = $('#' + $(this).closest('.carousel-nav').attr('data-target'));
			
			carousel.carousel(index);
			e.preventDefault();
		}
	);

	//========================== Activating Bootstrap Tabs ============================// 

    $('#tab1 a, #tab-content a').click(function (e) {
	    e.preventDefault();
	    $(this).tab('show');
    })


    //========================== SideBar Menu Children Slide In ============================// 

    $('.menu-widget ul li a, #responsive-nav ul li a').click( function (e){
    	$(this).find('span.icon').toggleClass(function() {
		    if ($(this).is('.awe-chevron-up')) {
                $(this).removeClass('awe-chevron-up');
		        return 'awe-chevron-down';
		    } else {
                $(this).removeClass('awe-chevron-down');
		        return 'awe-chevron-up';
		    }
		});
    	$(this).siblings('ul').slideToggle();
    });

    $('#responsive-nav .collapse-menu .collapse-trigger').click( function (e) {
        $(this).toggleClass(function() {
            if ($(this).is('.awe-chevron-down')) {
              $(this).removeClass('awe-chevron-down');
              return 'awe-chevron-up';
            } else {
              $(this).removeClass('awe-chevron-up');
              return 'awe-chevron-down';
            }
        });
        $(this).parent().siblings('ul').slideToggle();
    });


    //========================== Article Info Popover ============================// 

    $('.action.status span').popover({
    	animation: true,
    	html: true,
    	placement: 'left',
    	trigger: 'click',
    	content: function (i){
    		var status = $(this).data('status');
    		var content = "<div class='popover-desc'>" + status + "</div>";
    		return content;
    	}
    });

    $('.article-info .author-info span').popover({
    	animation: true,
    	html: true,
    	placement: 'left',
    	trigger: 'click',
    	content: function (i){
    		var src = $(this).data('image');
    		var author = $(this).data('author-desc');
    		var content = "<div class='popover-image image-polaroid'><img src='" + src + "' /></div><div class='popover-desc'>" + author + "</div>";
    		return content;
    	}
    });

    $('.article-info .time span').popover({
    	animation: true,
    	html: true,
    	placement: 'bottom',
    	trigger: 'click',
    	content: function(i) {
    		var date = $(this).data('date'),
    			day = date.day,
    			month = date.month,
    			year = date.year,
    			time = $(this).data('time');

    		var content = "<div class='popover-date'><span class='ent-calendar'></span>"+
    						month+" "+day+", "+year+"</div><div class='popover-time'>"+
    						"<span class='ent-clock'></span>"+time+"</div>";

    		return content;
    	}
    });

    $('.article-info .comment span').popover({
    	animation: true,
    	html: true,
    	placement: 'left',
    	trigger: 'click',
    	content: function(i) {
    		var data = $(this).data('comment-latest'),
    			author = data.author,
    			authorurl = data.authorurl,
    			comment = data.comment,
    			avatar = data.avatar;

    		var content = "<div class='info-title'><strong>Latest comment by:</strong></div>"+
    					  "<div class='popover-image image-polaroid'>" +
    					  "<img src='" + avatar + "' /></div>" +
    					  "<div class='popover-author'><a href='"+ authorurl + "' alt='"+author+"'>"+author+"</a></div>" +
    					  "<div class='popover-desc'>" + comment + "</div>";

    		return content;
    	}
    });

	//========================== Commnet Form ============================//

    $('input[type="text"], input[type="password"], input[type="email"], textarea').focus(function(){
    	$(this).parent('.input-border').addClass('focus');
    });
    $('input[type="text"], input[type="password"], input[type="email"], textarea').blur(function(){
    	$(this).parent('.input-border').removeClass('focus');
    });


    //========================== Article Info Popover ============================//
	
    //changeSpan();

	/*$(window).resize(function (){
		changeSpan();
	});*/

      
   $("#all").click(function(){
   	   $('.gallery-item').removeClass('last-col');
   	   $('.gallery-item:nth-child(4n+4)').addClass('last-col');
       $('.gallery-item').slideDown();
       $(this).parent().siblings().children('.active').removeClass('active');
       $(this).addClass("active");
       return false;
   });
   
   $(".filter").click(function(){
   		$('.gallery-item').slideUp();
   		$('.gallery-item').removeClass('last-col');

        var filter = $(this).attr("id");
        var i = 0;var j = 0;
        $('.'+filter).each(function(){
        		
        		if(i==3) {
        			j++;
	       			$('.'+filter).eq(i*j).addClass('last-col');
	       			i = 0;
	       		}
	       		i++;
	       		console.log("i", i);
	       		console.log("a",j);
        });
        $("."+ filter).slideDown();
        $(this).parent().siblings().children('.active').removeClass('active');
        $(this).addClass('active'); 

        return false;

   });
   
// document.ready END //	
});

function validate(){
	$.ajax({
		type:"POST",
		url:"/accounts/user_validate/ajax/",
		data:'value='+$('#txt_validar').val(),
		success: function(msg){
			if(msg != '0'){
				value = msg.split('|');

				$('#id_user').val(value[0]);
				$('#id_name').val(value[2] + ' ' + value[3]);
				$('#id_email').val(value[1]);
				$('#id_phone').val('');

				$('.msg_validate').addClass('ok');
				$('.msg_validate').html('Existe !!!');

				$('#id_email').attr('readonly', true);

				setTimeout(function(){
					$('.msg_validate').removeClass('ok');
					$('.msg_validate').html('');
				}, 3000)
			}else{
				$('.msg_validate').addClass('error');
				$('.msg_validate').html('No existe !!!');

				$('#id_user').val('');
				$('#id_name').val('');
				$('#id_email').val('');
				$('#id_email').attr('readonly', false);

				setTimeout(function(){
					$('.msg_validate').removeClass('error');
					$('.msg_validate').html('');
				}, 3000)
			}
		}
	});
}

function clean(){
	$('#id_user').val('');
	$('#id_name').val('');
	$('#id_email').val('');
	$('#txt_validar').val('');
	$('#id_email').attr('readonly', false);
}

function positionScroll(){
	if ($(window).scrollTop() != 0){
		$('.bar_top').addClass('fixed');
	}else{
		$('.bar_top').removeClass('fixed');
	}		
}

function whois(){
	$('.close').css({'display':'none'});
	$('#bg_whois').css({'height':$(document).height() + 500, 'display':'block'});
	$('body').css({'overflow':'hidden'});
	$('#whois').css({'display':'block', 'z-index':'1000'});
	$('#whois').addClass('in');
}

function whois_click(){
	$('#whois').css({'display':'block', 'z-index':'1000'});
	$('#bg_whois').css({'height':$(document).height() + 500, 'display':'block'});
	$('body').css({'overflow':'hidden'});
	$('#whois').addClass('in');
}
/*
function changeSpan() {
	
	$(".team .member").each(function() {
	  	if (Modernizr.mq('(min-width: 1200px)')) {
	    	$(this).attr('class', 'member span3');
	  	}
	  	
	  	if (Modernizr.mq('(max-width: 1180px) and (min-width:944px)')) {
	    	$(this).attr('class', 'member span4');
	  	}
	  	
	  	if (Modernizr.mq('(min-width: 768px) and (max-width: 979px)')) {
	   		$(this).attr('class', 'member span6');
	  	}
	});

	$(".footer-extra").each(function (i) {
		if (Modernizr.mq('(max-width: 1180px) and (min-width:944px)') || (Modernizr.mq('(min-width:1200px)'))) {
	    	$(this).attr('class', 'footer-extra span3');

	  		if(i == 2) {
	  			$(this).attr('class', 'footer-extra span2');
	  		}
	  	}

		if (Modernizr.mq('(min-width: 768px) and (max-width: 979px)')) {
	   		$(this).attr('class', 'footer-extra span4');
	  	}
	  	
	});

	if (Modernizr.mq('(min-width: 768px) and (max-width: 979px)')) {
   		if($('#slidejs').parent().is('.span8') || $('#cameraslide').parent().is('.span8')) {
   			$('#slidejs').parent().attr('class', 'span12');
   			$('#slidejs').find('.slide-outer').attr('class', 'slide-outer span12');
   			$('#cameraslide').parent().attr('class', 'span12');
   			$('#cameraslide').find('.camera-slide-wrapper').attr('class', 'camera-slide-wrapper span12');
   		}

   		if($('.home #content').is('.span6')) {
   			$('.home #content').attr('class', 'span8');
   		}

   		if($('#right-sidebar').is('.span3')) {
   			$('#right-sidebar').attr('class', 'span4');
   		}
  	}
  	else {
  		$('.home #content').attr('class', 'span6');
  		$('.home #right-sidebar').attr('class', 'span3');
  		$('#slidejs').parent().attr('class', 'span8');
  		$('#slidejs').find('.slide-outer').attr('class', 'slide-outer span8');
  		$('#cameraslide').parent().attr('class', 'span8');
  		$('#cameraslide').find('.camera-slide-wrapper').attr('class', 'camera-slide-wrapper span8');
  	}
}*/