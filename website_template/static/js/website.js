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

//mobile menu toggle
function openSideMenu() {
document.getElementById("mbl-menu-open").style.display = "block";
document.getElementById("mbl-menu-open").style.width = "88%";
}

function closeSideMenu() {
document.getElementById("mbl-menu-open").style.width = "0%";
document.getElementById("mbl-menu-open").style.display = "none";
}
