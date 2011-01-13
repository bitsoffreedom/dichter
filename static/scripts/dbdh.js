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
	  $('#vectors .selected').removeClass('selected');
	  $(this).parent().parent().addClass('selected');
	  $("#vectors li").addClass('disabled');
	  hidestepthree();
    $(this).parent().find('.contactVia li').each(function(){
	    var vector = this.className.substr(3).toLowerCase();
	    $("#via"+vector).removeClass('disabled');
	  });
	  return false;
	});
	
	$("#vectors li").click(function(){
	  if( $('#targets .selected').length == 0){
	    $('#targets').fadeTo(400, '.2').fadeTo(400, '1').fadeTo(400, '.2').fadeTo(400, '1');
	    return false;
	  }
    // get the id for the element we clicked on
    if($(this).hasClass('disabled')){
      return;
    }
    var vector = $(this).attr('id').substr(3).toLowerCase();
    hidestepthree();
    var payload = $('#targets .selected .via'+vector+' a').attr('href');
    var politician_name = $('#targets .selected h4').html();
    if(vector == 'email'){      
      if(payload.length > 0){
        $('#emailform form').attr('action', payload);
      }
	  $("#name").bind("focus", function (e) { 
	    if (e.currentTarget.value == e.currentTarget.getAttribute("value")) {
		  e.currentTarget.value = "";
		}
	  });
	  $("#name").bind("blur", function (e) { 
	    if (e.currentTarget.value == "") {
		  e.currentTarget.value = e.currentTarget.getAttribute("value");
		}
	  });
    }
    
    if(vector == 'phone'){
      if(payload.length > 0){
        $('#phone_name').html(politician_name);
        $('#phone_number').html(payload);
      }
    }
    
    if(vector == 'twitter'){      
      if(payload.length > 0){
        payload = "Geachte "+payload+
          ", [schrijf hier je oproep aan "+
          politician_name+
          "] "+
          $('#hero .hashtag').html();
      
        $('#'+vector+'form textarea').attr('value', payload);
      }     
    } 
    $('#'+vector+'form').show();
    // unset the current active vector
    $("#vectors .selected").removeClass('selected');
    // make the clicked vector active
    $(this).addClass('selected');
    return false;
  });
  
  // form validation #TODO
  $('#emailform .versturen input[type=submit]').click(function(){
    if($('#emailform textarea').value == ''){
      $('#emailform textarea').fadeTo(400, '.2').fadeTo(400, '1');      
      return false;
    };
    $('#thnx').show();
  });
}

function hidestepthree(){
  // hide all form parents (by lack of classes)
  $('#step3 .stepContent>div').each(function(){ 
    $(this).hide();
  });
  $('#thnx').hide();
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
