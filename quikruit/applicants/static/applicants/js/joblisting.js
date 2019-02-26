$(document).ready(function () {
	$('.descriptioncollapsebutton').click(function() {
		var idregex = /\_[a-z 0-9]*/;
		var id = idregex.exec($(this).attr('id'))[0];
		$('#desc' + id).slideToggle('slow');
		var buttonText = $('#collapse' + id).text();
		console.log(buttonText);
		if (buttonText === '▶︎ Description') {
			buttonText = '▼ Description'
		} else {
			buttonText = '▶︎ Description'
		}
		console.log(buttonText)
		$('#collapse' + id).text(buttonText);
	});
});