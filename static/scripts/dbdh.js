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

	//$('#targets .extraInfo').hide();
	var targets = $('#targets .extraInfo');

	for (i=0; i < targets.length; i++) {
		var src = targets[i];
//		var dst = $(targets[i]).prev()[0];
		var dst = src.cloneNode(false);
		src.parentNode.insertBefore(dst,src);
		$(dst).addClass("first");
		
		var children = $(src).children()
		var length = 0;
		for (j=0; j < children.length; j++) {
			if (length < 200) {
				dst.appendChild(children[j]);
				length = length + $(children[j]).text().length
			}
		}
		$(src).hide();
	}
	
	$('#targets .infoToggle a').click(function(e){
		e.preventDefault();
		$(this).closest('.infoToggle').prev().slideToggle(400,function () { $(this).trigger("scrollTo"); });
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



$("#vectors li").click(function(){
  // get the id for the element we clicked on
  if($(this).hasClass('disabled')){
    return;
  }
  vector = $(this).id.substr(3);
  // hide all form parents (by lack of classes)
  $('#step3 form').each(function(){ $(this).parentNode.hide()});
  $('#'+vector+'form').show();
  // unset the current active vector
  $("#vector .active").removeClass('active');
  // make the clicked vector active
  $(this).addClass('active');
})







