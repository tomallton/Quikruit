function isCSRFSafe(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
}

$(document).ready(function () {

  var csrfToken = Cookies.get('csrftoken');

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if(!isCSRFSafe(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken)
      }
    }
  });

  $('.collapsebutton').click(function() {
    var idregex = /\_[a-z 0-9\_]*/;
    var id = idregex.exec($(this).attr('id'))[0];
    $('#collapse' + id).slideToggle();
    var buttonText = $('#collapsebutton' + id).text().slice(1);
    var arrow = $('#collapsebutton' + id).text().slice(0,1);
    var newText = '';
    if (arrow === '▼') newText = '▶' + buttonText;
    else newText = '▼' + buttonText;
    $('#collapsebutton' + id).text(newText);
  });

  $('.addnew').click(function() {
    var idregex = /\_[a-z 0-9\_]*/;
    var id = idregex.exec($(this).attr('id'))[0];
    var extra_html;

    var new_form_number = $('#id' + id + '-TOTAL_FORMS').attr('value');
    extra_html = $('#emptyform' + id).html().replace(/__prefix__/g, new_form_number);
    $('#formset' + id).append(extra_html);
    $('#id' + id + '-TOTAL_FORMS').attr('value', parseInt(new_form_number) + 1);
  });

  $('body').on('click', '.skillhobbysuggestions li', function() {
    var skillhobbyid = $(this).attr('value')
    var skillhobbyslot = $(this).closest('.formcontainer').find('.skillhobbyslot')
    var skillhobbyname = $(this).text();
    var skillhobbyidcontainer
    skillhobbyslot.val(skillhobbyname);
    $(this).closest('.suggestionscontainer').height(0);
    skillhobbyslot.addClass('filled')
  });

  $('body').on('input', '.skillhobbyslot', function() {
    console.log($(this).val())
    form = $(this).parent();
    if ($(this).hasClass('filled')) {
      $(this).removeClass('filled');
    }
    if ($(this).val() === '') {
      $(form).find('.suggestionscontainer').height(0);
    } else {
    $.ajax(
      {
        url: 'skillhobby/',
        type: 'POST',
        data: {
          'skillhobby_filter': $(this).val().trim()}, 
        success: function(result){
          $(form).find('.skillhobbysuggestions').html(result);
          var height = $(form).find('.skillhobbysuggestions li').length*32
          $(form).find('.suggestionscontainer').height(height)
        }
      }
    );
  }
  });
});
