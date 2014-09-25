g_run_log_range = 0;
g_loading = false;
g_start_index = 0;

function change_run_log_range(id) {
    var button0 = "range0";
    var button1 = "range1";
    var button_id = "range" + id;
    console.log(button_id);
    g_run_log_range = id;

    $("#" + button0).attr('class', 'btn btn-default');
    $("#" + button1).attr('class', 'btn btn-default');
    $("#" + button_id).attr('class', 'btn btn-default active');
}

function load_run_log() {
    if (g_loading) {
	alert("请等待上次加载结束。");
    }
    g_loading = true;
    $.ajax({
	url: "/profile/more_log",
	type: "POST",
	data: { 'current_user': g_run_log_range, 'start_index': g_start_index },
	success: function(d, s, j) {
	    console.log(d);
	    g_loading = false;
	},
	error: function(j, s, e) {
	    g_loading = false;
	}
    });
}
