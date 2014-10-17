g_loading = false;
g_start_index = 0;

ITEM_COUNT = 30;

function load_run_log(id) {
    if (g_loading) {
	alert("请等待上次加载结束。");
	return ;
    }
    if (g_start_index == -1) {
	return ;
    }
    g_loading = true;
    $("#load-more").text("加载中...");
    $.ajax({
	url: "/profile/more_log",
	type: "POST",
	data: { 'current_user': 2, 'start_index': g_start_index, 'user_id': id },
	success: function(d, s, j) {

	    g_loading = false;
	    g_start_index += ITEM_COUNT;
	    $("#load-more").text("加载更多");

	    console.log(d);

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
		var tmp = '<li class="list-group-item" style="padding-left: 40px">'+json[i].username + ' 于 ' + json[i].date + ' ' + json[i].sport + ' ' + json[i].distance + ' km <a href="/runlog?runlog_id='+json[i].runlog_id+'">查看详情</a></li>';
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
}

function change_password() {
    var username = $("#c-username").val();
    var new_password = $("#c-new-p").val();
    var old_password = $("#c-old-p").val();

    if (new_password == "") {
	$("#c-status").text("请不要设置空密码");
    }

    $.ajax({
	url: "/user/change_password",
	type: "POST",
	data: {'username': username, 'new_password': new_password, 'old_password': old_password},
	success: function(d, s, j) {
	    console.log(d);
	    var json = $.parseJSON(d);
	    $("#c-status").text(json.result);
	},
	error: function(j, s, e) {
	    $("c-status").text("网络故障，请重试");
	}
    });
}
