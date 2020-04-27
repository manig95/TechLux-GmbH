

$(document).ready(function () {
	//   $('#wrap').css('opacity', '.3')
	$('.modalDialog').fadeIn();

	$('.close-popup').on('click', function (event) {
		event.preventDefault();
		/* Act on the event */
		$('.modalDialog').fadeOut(600);
		$('#wrap').css('opacity', 'unset')
	});

	$('.txt-thanks').on('click', function (event) {
		event.preventDefault();
		/* Act on the event */
		$('.modalDialog').fadeOut(600);
		$('#wrap').css('opacity', 'unset')
	});


	$('#view-code-btn').bind('click', function () {
		if ($('.js_subscribe_email').val() == '') {
		}
		else if(!validateEmail($('.js_subscribe_email').val())){
		}
		else {
			$.ajax({
				url: "/generate_signup_coupon/",
				type: 'POST',
				data: {email_id: $(".js_subscribe_email").val()},
				success: function (result) {
					$('#coupon').text(result);
				}
			});
			$('#coupon-code-view').hide();
			$('#coupon-code-view-show').show();
//			$('.o_notification_manager').hide();
		}
	});
});

 function validateEmail($email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return emailReg.test( $email );
}


//mobile menu toggle
function openSideMenu() {
	document.getElementById("mbl-menu-open").style.display = "block";
	document.getElementById("mbl-menu-open").style.width = "100%";
	$('#mb-menu-btn').attr('style', 'display: none !important');
	document.getElementById("mbl-menu-close").style.display = "block";
}

function closeSideMenu() {
	document.getElementById("mbl-menu-open").style.width = "0%";
	document.getElementById("mbl-menu-open").style.display = "none";
	document.getElementById("mb-menu-btn").style.display = "block";
	document.getElementById("mbl-menu-close").style.display = "none";
}


$(window).resize(function () {
	var test = $(window).width();
	if (test >= "971") {
		$('#mb-menu-btn').attr('style', 'display: none');
		$('#mbl-menu-open').attr('style', 'display: none !important');
		document.getElementById("mbl-menu-close").style.display = "none";
	} else {
		/*$('#mb-menu-btn').attr('style', 'display: block !important');*/
	}
});


copyContent = function (el) {
	var $tmp = $("<input />");
	$("body").append($tmp);
	$tmp.val($(el).text()).select();
	document.execCommand("copy");
	$('.txt-click-to-copy').text("COPIED")
	$('.txt-click-to-copy').css({
		'color': '#fff !important',
		'font-weight': 'bold'
	})
	$tmp.remove();
}

$('#coupon').on('click', function () {
	copyContent('#coupon');
});

