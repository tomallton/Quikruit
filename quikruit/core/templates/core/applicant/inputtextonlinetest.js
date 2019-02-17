$(document).ready(function() {

  $('#text_error').hide();

  var error_text = false;

  $('#answerslot').focusout(function() {
    check_field();
  });

  function check_field() {

    var value_length = $('#answerslot').val().length;

    if(value_length < 5 || value_length > 15) {
      error_text = true;
    }
    else {
      $('#text_error').hide();
      error_text = false;
    }

  }

  $('#answerform').submit(function() {

    error_text = false;

    check_field();

    if((error_text == false)) {
     return true;
    }
    else {
     $('#submit_error').html('Please enter an answer.');
     $('#submit_error').show();
     return false;
    }

  });

});
