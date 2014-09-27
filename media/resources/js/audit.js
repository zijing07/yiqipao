var g_current_run_log_id = "-1";

function reset() {
    $("#sport").text("");
    $("#distance").text("");
    $("#run_date").text("");
    $("#witness").text("");
    $("#picture").removeAttr("src");
    $("#comment").text("");
}

function click_item(num) {

    g_current_run_log_id = num
    
    $.ajax({
	url : "/audit/detail",
	type : "POST",
	data : { 'run_log_id': num },
	success : function(d, s, j) {
	    var json_data = $.parseJSON(d);
	    var data = json_data[0].fields;
	    $("#sport").text(data.sport);
	    $("#distance").text(data.distance);
	    $("#run_date").text(data.run_date.substr(0, 10));
	    $("#witness").text(data.witness);
	    $("#picture").attr("src", "/media/" + data.picture);
	    $("#comment").text(data.comment);
	},
	error : function(j, s, e) {
	    console.log("click item error!");
	    console.log(e);
	}
    });
}

function accept() {
    if (g_current_run_log_id == "-1") {
	alert("请先选择一个待审核项目。");
	return ;
    }
    $.ajax({
	url: "/audit/accept",
	type: "POST",
	data: { 'run_log_id': g_current_run_log_id },
	success : function(d, s, j) {
	    var json = $.parseJSON(d);
	    if (json.result == 'success') {
		$("#item"+g_current_run_log_id).css("display", "none");
		$("#system-info").text("操作成功");
		g_current_run_log_id = "-1";
		reset();
	    } else {
		$("#system-info").text("操作失败");
	    }
	},
	error: function (j, s, e) {
	    console.log("accept error");
	    console.log(e);
	    $("#system-info").text("操作成功");
	}
    });
}

function reject() {
    if (g_current_run_log_id == "-1") {
	alert("请先选择一个待审核项目。");
	return ;
    }
    $.ajax({
	url: "/audit/reject",
	type: "POST",
	data: { 'run_log_id': g_current_run_log_id },
	success : function(d, s, j) {
	    var json = $.parseJSON(d);
	    if (json.result == 'success') {
		$("#item"+g_current_run_log_id).css("display", "none");
		$("#system-info").text("操作成功");
		g_current_run_log_id = "-1";
		reset();
	    } else {
		$("#system-info").text("操作失败");
	    }
	},
	error: function (j, s, e) {
	    console.log("accept error");
	    console.log(e);
	    $("#system-info").text("操作失败");
	}
    });
}
