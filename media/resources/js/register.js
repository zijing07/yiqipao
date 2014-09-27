function validate_form() {
    var p1 = $("#password").val();
    var cp = $("#confirm-password");
    var p2 = cp.val();
    if (p1 != p2) {
	cp.popover('show');
	return false;
    }
    return true;
}
