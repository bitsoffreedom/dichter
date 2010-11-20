$(function () {
	function scrollPos () {
		var $t = $("#targets");
		if ($t.height() + $t[0].scrollTop == $t[0].scrollHeight) {
			return "bottom";
		} else if ($t[0].scrollTop == 0) {
			return "top";
		} else {
			return false;
		}
	}

	function navEnabler () {
		var position = scrollPos();
		$("#targetScrollUp").removeClass("ui-state-disabled");
		$("#targetScrollDown").removeClass("ui-state-disabled");

		if (position == "top") {
			$("#targetScrollUp").addClass("ui-state-disabled");
		} else if (position == "bottom") {
			$("#targetScrollDown").addClass("ui-state-disabled");
		}
	}
	function scrollUp (e) {
		var firstPartialTop = $.grep($("#targets > li"), function (e) {
			return ($(e).position().top < $("#targets").position().top) 
		}).reverse()[0]
		$(firstPartialTop).trigger("scrollTo");
	}
	function scrollDown (e) {
		var firstPartialBottom = $.grep($("#targets > li"), function (e) {
			return (($(e).position().top + $(e).height()) > ($("#targets").position().top + $("#targets").height()) ) 
		})[0]
		$(firstPartialBottom).trigger("scrollTo");
	}

	$("#targetScrollUp").click(scrollUp);
	$("#targetScrollDown").click(scrollDown);
	$("#targets").scroll(navEnabler);

	var targets = $("#targets > li");
	for (var i = 0; i < targets.length; i++) {
		$(targets[i]).bind("scrollTo", function (e) { 
			$(e.currentTarget).parent("ul").scrollTo(e.currentTarget, { duration: 500 })
		});
		$(targets[i]).click(function (e) {
			$(e.currentTarget).trigger("scrollTo");
		});
	}


	navEnabler();
});
