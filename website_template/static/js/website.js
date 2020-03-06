$( document ).ready(function() {
//   $('#wrap').css('opacity', '.3')
   $('.modalDialog').fadeIn();
    
    $('.close-popup').on('click', function(event) {
	  	event.preventDefault();
	  	/* Act on the event */
        $('.modalDialog').fadeOut(600);
        $('#wrap').css('opacity', 'unset')
	  });
});
