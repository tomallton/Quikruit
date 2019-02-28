$(document).ready(function () {
  $('.collapsebutton').click(function() {
    var idregex = /\_[a-z 0-9]*/;
    var id = idregex.exec($(this).attr('id'))[0];
    $('#collapse' + id).slideToggle();
    var buttonText = $('#collapsebutton' + id).text().slice(1);
    var arrow = $('#collapsebutton' + id).text().slice(0,1);
    var newText = '';
    if (arrow === '▼') newText = '▶' + buttonText;
    else newText = '▼' + buttonText;
    $('#collapsebutton' + id).text(newText);
  });
});

