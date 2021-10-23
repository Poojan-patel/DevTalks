$(function () {
	'use strict';

	$('.form-control').on('input', function () {
		var $field = $(this).closest('.form-group');
		if (this.value) {
			$field.addClass('field--not-empty');
		} else {
			$field.removeClass('field--not-empty');
		}
	});

	$('#username').change(function (e) {
		e.preventDefault();
		let value = $('#username').val();
		console.log(value);
		$.ajax({
			url: "/question/check_username/"+value,
			method: "POST",
			success: function(json){console.log(json)}
		});
	});

	$('#email').change(function (e) {
		e.preventDefault();
		let value = $('#email').val();
		console.log(value);
		$.ajax({
			url: "/question/check_email/"+value,
			method: "POST",
			success: function(json){console.log(json)}
		});
	});

	
});