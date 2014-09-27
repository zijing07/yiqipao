function mark_seen() {
    $.ajax({
	url: "/notification/mark_seen",
	type: "POST",
	success: function(d, s, j) {
	    console.log(d);
	    var json = $.parseJSON(d);
	    if (json.result == "success") {
		$("#noti-count").text(0);
	    } else {
		console.log("error!");
	    }
	},
	error: function(j, s, e) {
	    console.log(e);
	}
    });
