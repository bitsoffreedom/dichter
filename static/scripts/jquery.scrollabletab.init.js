var current_fragment = "";
$(function () {
		function load_content (url) {
			$('#content').fadeTo("slow",0.01, function () {
				$('#content').load(url + " #content", function () {
					var anchor = url.replace(/\/$/,"").replace(/.*\//,"");
					console.log(anchor);
					// Working around issues with jQuery related to naming the ID after the fragment
					$("#"+anchor).attr("id", "__fid");

					current_fragment = anchor;
					console.log(current_fragment);
					window.location = window.location.href.replace(/#?.*$/,"#" + anchor)

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
				console.log(url)
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
//			setTimeout(load_content_from_location, 1000);
		} else {
			var url = window.location.toString();
			current_fragment = url.replace(/.*\/([^\/])\/$/,"$1");
		}
})

