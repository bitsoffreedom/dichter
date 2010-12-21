function hero() {
	$('#hero .extraInfo').hide();
	$('#meer a').click(function(e){
		e.preventDefault();
		$('#hero .extraInfo').slideToggle();
		$('#meer').toggleClass('open');
		$(this).text($(this).text() == "Meer lezen" ? "Verbergen" : "Meer lezen");

	});

	var targets = $('#targets .extraInfo');

	for (var i=0; i < targets.length; i++) {
		var src = targets[i];
		var dst = src.cloneNode(false);
		src.parentNode.insertBefore(dst,src);
		$(dst).addClass("first");
		
		var children = $(src).children()
		var length = 0;
		for (var j=0; j < children.length; j++) {
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
	
	$('#targets .info a').click(function(){
	  $('#targets li').removeClass('selected');
	  $(this).parent().parent().addClass('selected');
	  $("#vectors li").addClass('disabled');
    $(this).parent().find('.contactVia li').each(function(){
	    var vector = this.className.substr(3).toLowerCase();
	    $("#via"+vector).removeClass('disabled');
	  });
	  return false;
	});
	
	$("#vectors li").click(function(){
    // get the id for the element we clicked on
    if($(this).hasClass('disabled')){
      return;
    }
    var vector = $(this).attr('id').substr(3).toLowerCase();
    // hide all form parents (by lack of classes)
    $('#step3 .stepContent>div').each(function(){ 
      $(this).hide();
    });
    $('#'+vector+'form').show();
    // unset the current active vector
    $("#vectors .selected").removeClass('selected');
    // make the clicked vector active
    $(this).addClass('selected');
    return false;
  });
}
$(document).ready(function(){
	hero();		
});

/* Keep tract of form size */
function field_size(field,size_field,limit) {
	if (field.value.length > limit) {
		field.value = field.value.substring(0, limit);
	} else {
		size_field.value = limit - field.value.length;
	}
}
