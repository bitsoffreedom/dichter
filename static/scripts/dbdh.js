$(document).ready(function(){
	
	$('#hero .extraInfo').hide();
	$('#meer a').click(function(e){
		e.preventDefault();
		$('#hero .extraInfo').slideToggle();
		$('#meer').toggleClass('open');
		$(this).text($(this).text() == "Meer lezen" ? "Verbergen" : "Meer lezen");

	});

	$('#targets .extraInfo').hide();
	$('#targets .infoToggle a').click(function(e){
		e.preventDefault();
		$(this).closest('.infoToggle').prev().slideToggle();
		$(this).closest('.infoToggle').toggleClass('hide');
		$(this).text($(this).text() == "Meer informatie" ? "Informatie verbergen" : "Meer informatie");
	});
	
});
