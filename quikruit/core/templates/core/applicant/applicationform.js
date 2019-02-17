$(document).ready(function() {

  $('#name_error').hide();
  $('#degreequalification_error').hide();
  $('#degreelevel_error').hide();
  $('#university_error').hide();
  $('#alevel_error').hide();
  $('#language_error').hide();
  $('#expertise_error').hide();
  $('#previousemployer_error').hide();
  $('#positionheld_error').hide();
  $('#lengthofemployment_error').hide();
  $('#skills_error').hide();
  $('#hobbies_error').hide();

  var error_name = false;
  var error_degreequalification = false;
  var error_degreelevel = false;
  var error_university = false;
  var error_alevel = false;
  var error_language = false;
  var error_expertise = false;
  var error_previousemployer = false;
  var error_positionheld = false;
  var error_lengthofemployment = false;
  var error_skills = false;
  var error_hobbies = false;

  $('#nameslot').focusout(function() {
    value('#nameslot', '#name_error', error_name);
  });

  $('#degreequalificationslot').focusout(function() {
    value('#degreequalificationslot', '#degreequalification_error', error_degreequalification);
  });

  $('#degreelevelslot').focusout(function() {
    value('#degreelevelslot', '#degreelevel_error', error_degreelevel);
  });

  $('#universityslot').focusout(function() {
    value('#universityslot', '#university_error', error_university);
  });

  $('#alevelslot').focusout(function() {
    value('#alevelslot', '#alevel_error', error_alevel);
  });

  $('#languageslot').focusout(function() {
    value('#languageslot', '#language_error', error_language);
  });

  $('#expertiseslot').focusout(function() {
    value('#expertiseslot', '#expertise_error', error_expertise);
  });

  $('#previousemployerslot').focusout(function() {
    value('#previousemployerslot', '#previousemployer_error', error_previousemployer);
  });

  $('#positionheldslot').focusout(function() {
    value('#positionheldslot', '#positionheld_error', error_positionheld);
  });

  $('#employmentlengthslot').focusout(function() {
    value('#employmentlengthslot', '#lengthofemployment_error', error_lengthofemployment);
  });

  $('#skillslot').focusout(function() {
    value('#skillslot', '#skills_error', error_skills);
  });

  $('#hobbieslot').focusout(function() {
    value('#hobbieslot', '#hobbies_error', error_hobbies);
  });

  function value(slot, error, variable) {

    var valuelength = $(slot).val().length;

    if(valuelength == 0) {
      $(error).html('This field is required.');
      $(error).show();
      variable = true;
    }
    else {
      $(error).hide();
      variable = false;
    }

    return variable;

  }

  $('#applicationform').submit(function() {

    error_name = false;
    error_degreequalification = false;
    error_degreelevel = false;
    error_university = false;
    error_alevel = false;
    error_language = false;
    error_expertise = false;
    error_previousemployer = false;
    error_positionheld = false;
    error_lengthofemployment = false;
    error_skills = false;
    error_hobbies = false;

    error_name = value('#nameslot', '#name_error', error_name);
    error_degreequalification = value('#degreequalificationslot', '#degreequalification_error', error_degreequalification);
    error_degreelevel = value('#degreelevelslot', '#degreelevel_error', error_degreelevel);
    error_university = value('#universityslot', '#university_error', error_university);
    error_alevel = value('#alevelslot', '#alevel_error', error_alevel);
    error_language = value('#languageslot', '#language_error', error_language);
    error_expertise = value('#expertiseslot', '#expertise_error', error_expertise);
    error_previousemployer = value('#previousemployerslot', '#previousemployer_error', error_previousemployer);
    error_positionheld = value('#positionheldslot', '#positionheld_error', error_positionheld);
    error_lengthofemployment = value('#employmentlengthslot', '#lengthofemployment_error', error_lengthofemployment);
    error_skills = value('#skillslot', '#skills_error', error_skills);
    error_hobbies = value('#hobbieslot', '#hobbies_error', error_hobbies);

    if((error_name == false) && (error_degreequalification == false) && (error_degreelevel == false) && (error_university == false) && (error_alevel == false) && (error_language == false) && (error_expertise == false) && (error_previousemployer == false) && (error_positionheld == false) && (error_lengthofemployment == false) && (error_skills == false) && (error_hobbies == false)) {
     return true;
    }
    else {
     $('#submit_error').html('Please ensure all the fields are completed');
     $('#submit_error').show();
     return false;
    }

  });

});
