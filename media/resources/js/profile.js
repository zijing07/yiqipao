g_run_log_range = 0;
g_loading = false;
g_start_index = 0;

ITEM_COUNT = 2;

function change_run_log_range(id) {
    var button0 = "range0";
    var button1 = "range1";
    var button_id = "range" + id;
    console.log(button_id);
    g_run_log_range = id;
    g_start_index = 0;

    $("#" + button0).attr('class', 'btn btn-default');
    $("#" + button1).attr('class', 'btn btn-default');
    $("#" + button_id).attr('class', 'btn btn-default active');

    $("#run-logs").html("");

    load_run_log();
}

function load_run_log() {
    if (g_loading) {
	alert("请等待上次加载结束。");
    }
    if (g_start_index == -1) {
	return ;
    }
    g_loading = true;
    $("#load-more").text("加载中...");
    $.ajax({
	url: "/profile/more_log",
	type: "POST",
	data: { 'current_user': g_run_log_range, 'start_index': g_start_index },
	success: function(d, s, j) {

	    g_loading = false;
	    g_start_index += ITEM_COUNT;
	    $("#load-more").text("加载更多");

	    var json = $.parseJSON(d);
	    if (json.result != undefined) {
		$("#load-more").text("加载失败，点击重试");
		return ;
	    }

	    var len = json.length;

	    if (len == 0) {
		g_start_index = -1;
		$("#load-more").text("没有更多");
	    }
	    
	    var html = '';
	    for (var i=0; i<len; ++i) {
		var tmp = '<li class="list-group-item" style="padding-left: 40px">'+json[i].username + ' 于 ' + json[i].date + ' ' + json[i].sport + ' ' + json[i].distance + ' km</li>';
		html += tmp;
	    }
	    var h = $("#run-logs").html() + html;
	    $("#run-logs").html(h);
	},
	error: function(j, s, e) {
	    $("#load-more").text("加载失败，点击重试");
	    g_loading = false;
	}
    });
}
