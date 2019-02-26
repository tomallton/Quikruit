$(document).ready(function () {
	$('.descriptioncollapsebutton').click(function() {
		console.log('clickbutton')
		$('.jobdescription').slideToggle('slow');
	});
});