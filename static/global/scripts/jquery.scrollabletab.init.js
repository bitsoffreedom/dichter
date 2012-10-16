var current_fragment = "";
$(function () {
	/* Work around bug in IE */
	$.fn.customFadeTo=  function(speed, end, callback)  {
    	$(this).fadeTo(speed, end,  function()  {
    	    if(!$.support.opacity)
        	    $(this).get(0).style.removeAttribute('filter');
        	if(callback!=  undefined)
            	callback();
	    });
	};

	/* Utility functions */
	/* Does not work for now */
	function scrollPos () {
		return false;
		var $t = $("#campagnes-list");
		if ($t.width() + $t[0].scrollLeft == $t[0].scrollWidth) {
			return "right";
		} else if ($t[0].scrollLeft == 0) {
			return "left";
		} else {
			return false;
		}
	}

	
	function navEnabler () {
		var position = scrollPos();
		$("#campagnesScrollLeft").removeClass("ui-state-disabled");
		$("#campagnesScrollRight").removeClass("ui-state-disabled");

		if (position == "left") {
			$("#campagnesScrollLeft").addClass("ui-state-disabled");
		} else if (position == "right") {
			$("#campagnesScrollRight").addClass("ui-state-disabled");
		}
	}
	
	/* Events on buttons */
	function scrollLeft (e) {
		var firstPartialLeft = $.grep($("#campagnes-list li"), function (e) {
			return ($(e).position().left < 0);
		}).reverse()[0]
		$(firstPartialLeft).trigger("scrollTo"); 
	}
	function scrollRight (e) {
		var firstPartialRight = $.grep($("#campagnes-list li"), function (e) {
			return (($(e).position().left + $(e).width()) > $("#campagnes-list").width()) ;
		})[0]
		$(firstPartialRight).trigger("scrollTo"); 
		
	}

	$("#campagnesScrollLeft").click(scrollLeft);
	$("#campagnesScrollRight").click(scrollRight);

	
	/* Events bound to each tab */
	var targets = $("#campagnes-list ul > li");
	for (var i = 0; i < targets.length; i++) { 
		$(targets[i]).bind("scrollTo", function (e) { 

			if ($(e.currentTarget).position().left < 0) {
				$("#campagnes-list").scrollTo($(e.currentTarget), 500, { axis: "x", onAfter: navEnabler })
			} else if (($(e.currentTarget).position().left + $(e.currentTarget).width()) > $("#campagnes-list").width()) {
				$("#campagnes-list").scrollTo(e.currentTarget, 500, {offset: {left: 0 - ( $("#campagnes-list").width() - $(e.currentTarget).width() ) }, axis: "x", onAfter: navEnabler })
			}
			navEnabler();
		});

		$(targets[i]).click(function (e) {
			var link = $(e.currentTarget).find("a")[0]
			load_tab(link);
			return false;
		});
	}

	function load_tab (link) {
		__change_running = true;

		highlight_tab($(link).parent("li"));
		$(link).parent("li").trigger("scrollTo");

		window.location = window.location.href.replace(/#?.*$/,"#" + link.title)

		if (link) {
			load_content(link);
		} 
	
		current_fragment = link.title;

		__change_running = false;
	}
	
	function load_content (link) {
		$('#content').customFadeTo("slow",0.01, function () {
			$('#content').load(link.href + " #content", function () {

				var anchor = link.title;
				
				// Working around issues with jQuery related to naming the ID after the fragment
				$("#"+anchor).attr("id", "__fid");

				hero();

				$('#content').customFadeTo("slow",1);
				// Release hash change lock here due to asynchronicity
			});
		});
	}

	function highlight_tab(link) {
		/* Highlight relevant tab */
		$(".ui-state-active").removeClass("ui-state-active");
		$(link).addClass("ui-state-active");
	}

	// Handle forward/backwards navigation 
	__change_running = false;
	function hash_change () {
		if (__change_running) { return; }
		var location = window.location.toString()
	
		if (location.match(/#(.+$)/)) {
			var anchor = decodeURIComponent(location.match(/#(.+$)/)[1]);
		} else if (current_fragment != "") {
			__change_running = true;

			var link = $("#campagnes-list a:first-child")[0];

			highlight_tab($(link).parent("li"));
			load_content(link);
			current_fragment = "";
			__change_running = false;
		}
		
		if (anchor && !anchor.match("^" + current_fragment + "$")){
			var link = $("a[title=" + decodeURIComponent(window.location.toString().match(/#(.+)$/)[1]) + "]")[0]

			load_tab(link);
		}
	}
	if ("onhashchange" in window) {
		window.onhashchange = hash_change;
	} else {
		hash_change_check_interval = setInterval(hash_change, 200);
	}

	/* XXX quick hack
	 * Hide nav buttons entirely if the list is smaller then it's container 
	 */
	(function () {
		var campagnes_width = 0;
		var campagnes = $("#campagnes-list li");
		for (var i = 0; i < campagnes.length; ++i) {
			campagnes_width += $(campagnes[i]).width();
		}
		if (campagnes_width < $("#campagnes-list").width()) {
			$("#campagnesScrollLeft").hide();
			$("#campagnesScrollRight").hide();
		}
	})();
	/* First campaign highlighted, should be done in CSS, isn't */
	$("#campagnes-list li:first-child").addClass("ui-state-active");

	/* Enable correct nav buttons */	
	navEnabler();
})
