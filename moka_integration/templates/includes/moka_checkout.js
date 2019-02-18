var moka_sanbox = "{{moka_sandbox}}";

$("#devamEt").click(function() {
	var args = {};
	args.token = "{{token}}";
	args.name = $('#card-name').val();
	args.number = $('#mokacardnumber').val();
	args.expiry = $('#expiry').val();
	args.cvc = $('#cvc').val();
	args.amount = "{{ amount }}";
	args.OtherTrxCode = "{{ order_id }}";
	args.currency = "{{ currency }}";
	

	frappe.call({
		method:"moka_integration.templates.pages.moka_checkout.make_checkout",
		args: {data:args},
		callback: function(r){
			console.log(r.message);
			if (r.message && r.message.ResultCode == "Success") {
				window.location.href = r.message.Data
			}
			else{
				if(r.message) {
					frappe.msgprint(r.message.ResultCode)
				}
			}
		}
	})
	return false;
});

new Card({
	form: document.querySelector('.hepsi'),
	container: '.card-wrapper',
	formSelectors: {

		nameInput: 'input#card-name'
	},

});
$(document).ready(function () {
	$('input[type=radio][name=mokatotal]').change(function () {

		$('.mokaOdemeTutar').text(this.value);

	});
});

$(".moka-i-icon img").hover(function () {
	$(".info-window").toggleClass("info-window-active");
});

$('.c-card').bind('keypress keyup keydown focus', function (e) {
	var ErrorInput = false;
	if ($("input.card-name").hasClass("jp-card-invalid")) {
		ErrorInput = true;
		$("input.card-name").addClass("border");
	}
	if ($("input.cardnumber").hasClass("jp-card-invalid")) {
		ErrorInput = true;
		$("input.cardnumber").addClass("border");
	}
	if ($("input.c-date").hasClass("jp-card-invalid")) {
		ErrorInput = true;
		$("input.c-date").addClass("border");
	}
	if ($("input.card-cvc").hasClass("jp-card-invalid")) {
		ErrorInput = true;
		$("input.card-cvc").addClass("border");
	}

	if (ErrorInput === true && moka_sanbox!="1") {
		$('.mokaode').attr("disabled", true);
		$(".mokaode").css("opacity", "0.5");

	} else {

		$("input.card-name").removeClass("border");
		$("input.cardnumber").removeClass("border");
		$("input.c-date").removeClass("border");
		$("input.card-cvc").removeClass("border");
		$('.mokaode').attr("disabled", false);
		$(".mokaode").css("opacity", "1");

	}

});



