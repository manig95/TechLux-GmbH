$( document ).ready(function() {
//   $('#wrap').css('opacity', '.3')
   $('.modalDialog').fadeIn();
    
    $('.close-popup').on('click', function(event) {
	  	event.preventDefault();
	  	/* Act on the event */
        $('.modalDialog').fadeOut(600);
        $('#wrap').css('opacity', 'unset')
	  });


    $('#view-code-btn').click(function() {
//        $('#coupon-code-view').css("display", "none");
          $('#coupon-code-view').hide();
          $('#coupon-code-view-show').show();
    });

	/*$('#view-code-btn').bind('click', function(){
        $.ajax({
            url: "/send_category_enquiry/",
             type: 'POST',
             data: {comment: $(".pt_description").val(),email_id: $("#mail_id").val(),name: $("#name").val(),search_string: $(".search-query").val()},
             success: function(result){
                 if (result =='mail_sent') {
                   $('#coupon-code-view').hide();
                   $('#coupon-code-view-show').show();
                  } else {
                      alert("Mail not sent, Please try after some time");
                  }
             }});
    });*/
});

//mobile menu toggle
function openSideMenu() {
document.getElementById("mbl-menu-open").style.display = "block";
document.getElementById("mbl-menu-open").style.width = "88%";
$('#mb-menu-btn').attr('style','display: none !important');
document.getElementById("mbl-menu-close").style.display = "block";
}

function closeSideMenu() {
document.getElementById("mbl-menu-open").style.width = "0%";
document.getElementById("mbl-menu-open").style.display = "none";
document.getElementById("mb-menu-btn").style.display = "block";
document.getElementById("mbl-menu-close").style.display = "none";
}


$( window ).resize(function() {
var test = $( window ).width();
if( test >= "971" ){
$('#mb-menu-btn').attr('style','display: none !important');
document.getElementById("mbl-menu-close").style.display = "none";
}
else{
$('#mb-menu-btn').attr('style','display: block !important');
}
});