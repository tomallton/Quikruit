$(document).ready(function() {

  $('#username_error').hide();
  $('#email_error').hide();
  $('#password_error').hide();
  $('#confirmpassword_error').hide();

  var error_username = false;
  var error_email = false;
  var error_password = false;
  var error_confirmpassword = false;

  $('#registerslot').focusout(function() {
    check_username();
  });

  $('#emailslot').focusout(function() {
    check_email();
  });

  $('#passwordslot').focusout(function() {
    check_password();
  });

  $('#confirmpasswordslot').focusout(function() {
    check_confirmpassword();
  });

  function check_username() {

    var username_length = $('#registerslot').val().length;

    if(username_length < 5 || username_length > 15) {
      $('#username_error').html('Username should be between 5-15 characters.');
      $('#username_error').show();
      error_username = true;
    }
    else {
      $('#username_error').hide();
      error_username = false;
    }

  }

  function check_email() {

    var string = new RegExp(/^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i);

    if(string.test($('#emailslot').val())) {
      $('#email_error').hide();
      error_email = false;
    }
    else {
      $('#email_error').html('Invalid email ID.');
      $('#email_error').show();
      error_email = true;
    }
  }

   function check_password() {

    var password_length = $('#passwordslot').val().length;

    if(password_length < 5) {
      $('#password_error').html('Password should be atleast 4 characters.');
      $('#password_error').show();
      error_password = true;
    }
    else {
      $('#password_error').hide();
      error_password = false;
    }

  }

  function check_confirmpassword() {

    var password = $('#passwordslot').val();
    var confirmpassword = $('#confirmpasswordslot').val();

    if(password != confirmpassword) {
      $('#confirmpassword_error').html('Passwords do not match.');
      $('#confirmpassword_error').show();
      error_confirmpassword = true;
    }
    else {
      $('#confirmpassword_error').hide();
      error_confirmpassword = false;
    }

  }

  $('#registerform').submit(function() {

    error_username = false;
    error_email = false;
    error_password = false;
    error_confirmpassword = false;

    check_username();
    check_email();
    check_password();
    check_confirmpassword();

    if((error_username == false) && (error_email == false) && (error_password == false) && (error_confirmpassword == false)) {
     return true;
    }
    else {
     $('#submit_error').html('Please enter valid details.');
     $('#submit_error').show();
     return false;
    }

  });

});
