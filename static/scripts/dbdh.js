function hero() {
	$('#hero .extraInfo').hide();
	$('#meer a').click(function(e){
		e.preventDefault();
		$('#hero .extraInfo').slideToggle();
		$('#meer').toggleClass('open');
		$(this).text($(this).text() == "Meer lezen" ? "Verbergen" : "Meer lezen");

	});
}
$(document).ready(function(){
	hero();	

	$('#targets .extraInfo').hide();
	$('#targets .infoToggle a').click(function(e){
		e.preventDefault();
		$(this).closest('.infoToggle').prev().slideToggle();
		$(this).closest('.infoToggle').toggleClass('hide');
		$(this).text($(this).text() == "Meer informatie" ? "Informatie verbergen" : "Meer informatie");
	});
	
});

/* Keep tract of form size */
function field_size(field,size_field,limit) {
	if (field.value.length > limit) {
		field.value = field.value.substring(0, limit);
	} else {
		size_field.value = limit - field.value.length;
	}
}

