function new_employment_template(n) {
  return `<label for="id_prior_employment-${n}-company">Company:</label>
  <input type="text" name="prior_employment-${n}-company" maxlength="60" id="id_prior_employment-${n}-company">
  <label for="id_prior_employment-${n}-position">Position:</label>
  <input type="text" name="prior_employment-${n}-position" maxlength="60" id="id_prior_employment-${n}-position">
  <label for="id_prior_employment-${n}-employment_length">Employment length:</label>
  <input type="text" name="prior_employment-${n}-employment_length" id="id_prior_employment-${n}-employment_length">
  <label for="id_prior_employment-${n}-DELETE">Delete:</label>
  <input type="checkbox" name="prior_employment-${n}-DELETE" id="id_prior_employment-0-DELETE">
  <input type="hidden" name="prior_employment-${n}-applicant" value="8l8va8rii5idixi" id="id_prior_employment-${n}-applicant">
  <input type="hidden" name="prior_employment-${n}-id" id="id_prior_employment-${n}-id">`;
}

function new_degree_template(n) {
  return `<label for="id_degree-${n}-institution">Institution:</label>
  <input type="text" name="degree-${n}-institution" maxlength="60" id="id_degree-${n}-institution">
  <label for="id_degree-${n}-qualification">Qualification:</label>
  <input type="text" name="degree-${n}-qualification" maxlength="60" id="id_degree-${n}-qualification">
  <label for="id_degree-${n}-level_awarded">Level Awarded:</label>
  <input type="text" name="degree-${n}-level_awarded" id="id_degree-${n}-level_awarded">
  <label for="id_degree-${n}-DELETE">Delete:</label>
  <input type="checkbox" name="degree-${n}-DELETE" id="id_degree-0-DELETE">
  <input type="hidden" name="degree-${n}-applicant" value="8l8va8rii5idixi" id="id_degree-${n}-applicant">
  <input type="hidden" name="degree-${n}-id" id="id_degree-${n}-id">`;
}

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

  employment_count = parseInt($('#id_prior_employment-TOTAL_FORMS').attr('value'));
  degree_count = parseInt($('#id_degree-TOTAL_FORMS').attr('value'));
  alevel_count = parseInt($('#id_a_levels-TOTAL_FORMS').attr('value'));
  skillhobby_count = parseInt($('#id_skill_hobby_levels-TOTAL_FORMS').attr('value'));

  $('.addnew').click(function() {
    console.log($(this).attr('id'));
    var idregex = /\_[a-z 0-9]*/;
    var id = idregex.exec($(this).attr('id'))[0];
    var formset_html = $('#formset' + id).html();

    var extra_html;

    switch (id) {
      case '_employment':
        alert("hi hello employer");
        extra_html = new_employment_template(employment_count);
        employment_count += 1;
        $('#id_prior_employment-TOTAL_FORMS').attr('value', `${employment_count}`);
        break;
      case '_degree':
        alert("hi hello ployer");
        extra_html = new_degree_template(degree_count);
        degree_count += 1;
        $('#id_degree-TOTAL_FORMS').attr('value', `${degree_count}`);
        break;
      case '_alevel':
        extra_html = new_alevel_template(alevel_count);
        alevel_count += 1;
        $('#id_alevel-TOTAL_FORMS').attr('value', `${alevel_count}`);
        break;
      case '_skillhobby':
        extra_html = new_skillhobby_template(skillhobby_count);
        skillhobby_count += 1;
        $('#id_skillhobby-TOTAL_FORMS').attr('value', `${skillhobby_count}`);
        break;
      default:
        break;
    }

    var new_form = new_employment_template(employment_count);
    $('#formset' + id).html(formset_html + extra_html);
    console.log($('#formset' + id).html());

    var new_form = new_degree_template(degree_count);
    $('#formset' + id).html(formset_html + extra_html);
    console.log($('#formset' + id).html());

    var new_form = new_alevel_template(alevel_count);
    $('#formset' + id).html(formset_html + extra_html);
    console.log($('#formset' + id).html());

    var new_form = new_skillhobby_template(skillhobby_count);
    $('#formset' + id).html(formset_html + extra_html);
    console.log($('#formset' + id).html());
  });
});
