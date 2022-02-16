// const signUpButton = document.getElementById('signUp');
// const signInButton = document.getElementById('signIn');
// const container = document.getElementById('container');
//
// signUpButton.addEventListener('click', () => {
// 	container.classList.add("right-panel-active");
// });
//
// signInButton.addEventListener('click', () => {
// 	container.classList.remove("right-panel-active");
// });


$("#id_username").change(function () {
      var username = $(this).val();

      $.ajax({
        url: '/ajax/validate_username/',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (data) {
          if (data.is_taken) {
            alert(data.error_message);
          }
        }
      });

    });

$("#id_email").change(function () {
      var email = $(this).val();

      $.ajax({
        url: '/ajax/validate_username/',
        data: {
          'email': email
        },
        dataType: 'json',
        success: function (data) {
          if (data.is_taken) {
            alert("A user with this username already exists.");
          }
        }
      });

    });