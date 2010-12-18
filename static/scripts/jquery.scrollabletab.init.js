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
	function scrollPos () {
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
			$(e.currentTarget).trigger("scrollTo");
			var link = $(e.currentTarget).find("a")[0]
			highlight_tab(e.currentTarget);
			load_content(link);
			return false;
		});
	}

	function load_content (link) {
		$('#content').customFadeTo("slow",0.01, function () {
			$('#content').load(link.href + " #content", function () {

				var anchor = link.title;
				
				// Working around issues with jQuery related to naming the ID after the fragment
				$("#"+anchor).attr("id", "__fid");

				current_fragment = anchor;
				window.location = window.location.href.replace(/#?.*$/,"#" + anchor)
				
				hero();

				$('#content').customFadeTo("slow",1);
				// Release hash change lock here due to asynchronicity
				__hash_change_running = false;
			});
		});
	}

	function highlight_tab(link) {
		/* Highlight relevant tab */
		$(".ui-state-active").removeClass("ui-state-active");
		$(link).addClass("ui-state-active");
	}

	// Handle forward/backwards navigation 
	__hash_change_running = false;
	function hash_change () {
		if (__hash_change_running) { return; }
		var location = window.location.toString()
		if (location.match(/#.+$/) && !location.match("#" + current_fragment + "$")){
			// Prevent from running multiple updates at once
			__hash_change_running = true;


			var link = $("a[title=" + window.location.toString().match(/#(.+)$/)[1] + "]")[0]
			highlight_tab($(link).parent("li"));

			if (link) {
				load_content(link);
			} else {
				return;
			}
		}/* else if (location.match("/$") && !location.match("/" + current_fragment + "/$") && !location.match("//[^/]/$)) {
			__hash_change_running = true;

			var link = $("#logo a")[0];
			if (link) {
				load_content(link);
			} else {
				return;
			}
		}*/
	}
	if ("onhashchange" in window) {
		window.onhashchange = hash_change;
	} else {
		hash_change_check_interval = setInterval(hash_change, 200);
	}

	/* Enable correct nav buttons */	
	navEnabler();
})
/*$(function () {
		function load_content (url) {
			$('#content').fadeTo("slow",0.01, function () {
				$('#content').load(url + " #content", function () {
					var anchor = url.replace(/\/$/,"").replace(/.*\//,"");
					// Working around issues with jQuery related to naming the ID after the fragment
					$("#"+anchor).attr("id", "__fid");

					current_fragment = anchor;
					window.location = window.location.href.replace(/#?.*$/,"#" + anchor)

					hero();
					$('#content').fadeTo('slow',1);
					// Release hash change lock here due to asynchronicity
					__hash_change_running = false;
				})
			})
		}
			
		function load_content_from_location () {
			var fragment = window.location.toString();
			fragment = "#" + fragment.replace(/.*#/,"");
			$('#campagnes-list').tabs('select',$('#campagnes-list a[href=' + fragment + ']').parent().prevAll().length);
		}
			
		$('#campagnes-list').tabs({
			ajaxOptions: { beforeSend: function () { return false } },
			select: function(event, ui) {
				var url = ui.tab.getAttribute("href");
				url = "/campaign/" + url.replace(/^#/,"") + "/"; 

				// Working around issues with jQuery related to naming the ID after the fragment
				$("#__fid").attr("id", current_fragment);
				load_content(url)
				return true;
			}
		}).scrollabletab();
	
		__hash_change_running = false;

		function hash_change () {
			if (__hash_change_running) { return; }
			var location = window.location.toString()
			if (location.match(/#.+$/) && !location.match("#" + current_fragment + "$")){
				// Prevent from running multiple updates at once
				__hash_change_running = true;
				load_content_from_location();
			} else if (location.match("/$") && !location.match("/" + current_fragment + "/$")) {
				__hash_change_running = true;
				load_content_from_location();
			}
		}
		if ("onhashchange" in window) {
			window.onhashchange = hash_change;
		} else {
			hash_change_check_interval = setInterval(hash_change, 200);
		}

// Load correct tab on load
		if (window.location.toString().match(/#.+$/)) {
			var fragment = window.location.toString();
			fragment = "#" + fragment.replace(/.*#/,"");
			var url = "/campaign/" + fragment.replace(/^#/,"") + "/";
			load_content(url)
		} else {
			var url = window.location.toString();
			current_fragment = url.replace(/.*\/([^\/]+)\/$/,"$1");
			var current_tab = $("[href=#" + current_fragment + "]")[0].parentNode;
			var clean_style = current_tab.className;
			current_tab.className = $("#campagnes-list li")[0].className;
			$("#campagnes-list li")[0].className = clean_style;

		}

		$("#campagnes-list").trigger('scrollToTab',$("#campagnes-list li.ui-tabs-selected"));
		$("#campagnes-list").trigger('navEnabler'); 
})
*/
