$(document).ready(function() {

  $('#username_error').hide();
  var username_error = false;
  $('#password_error').hide();
  var password_error = false;

  $('#loginslot').focusout(function () {

    check_username();

  });

  $('#passwordslot').focusout(function() {

    check_password();

  });

  function check_username() {
   if($('#loginslot').val() == "") {
      $('#username_error').html("Please enter your Username.");
      $('#username_error').show();
      username_error = true;
    }
    else {
      $('#username_error').hide();
      username_error = false;
    }
  }

  function check_password() {
    if($('#passwordslot').val() == "") {
      $('#password_error').html("Please enter your Password.");
      $('#password_error').show();
      password_error = true;
    }
    else {
      $('#password_error').hide();
      password_error = false;
    }

  }

  $('#loginform').submit(function() {

    password_error = false;
    username_error = false;

    check_username();
    check_password();

    if((username_error == false) && (password_error == false)) {
     return true;
    }
    else {
     $('#submit_error').html('Please fill in all the required fields.');
     $('#submit_error').show();
     return false;
    }

  });

});
