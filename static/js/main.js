var hide = {
    login: function(){
        $('#login').modal('close');
        $('#loginbtn').hide();
        $('#sideNavbtn').show();
    },
    user: function(){
        $('#sideNavbtn').hide();
        $('#loginbtn').show();

    }
}
if(logged){
  hide.login();
}
else{
  hide.user();
}

var messages = {
    "dataNotFound": "Invalid Song Details!",
    "incompleteFields": "Fill out all required fields!",
    "notConnected": "User Already Disconnected",
    "successLogout": "User Successfully Logged Out",
    "notLogged" : "User Not Logged In",
    "notAuth" : "App not authenticated"
};

$('.button-collapse').sideNav({

      menuWidth: 240,

      edge: 'left',

      closeOnClick: true,

      draggable: true
    }
  );

$(document).ready(function(){

    $('.modal').modal();

    $('.ani-shadow').hover(function(){

        $(this).toggleClass('z-depth-4').toggleClass('z-depth-1');

    });

     $('select').material_select();

    function getQueryVariable(variable)
        {
               var query = window.location.search.substring(1);
               var vars = query.split("&");
               for (var i=0;i<vars.length;i++) {
                       var pair = vars[i].split("=");
                       if(pair[0] == variable){return pair[1];}
               }
               return(false);
        }


        if(getQueryVariable('error')){

            var error = messages[getQueryVariable('error')];

             Materialize.toast(error, 10000);

        }

        $("#fbSignIn").click(function(){
            FB.login(function(response){
              checkFBStatus();
            },{scope: 'email,public_profile'})
        });

 });


var checkFBStatus = function(){
  FB.getLoginStatus(function(response) {
      if (response.status === 'connected') {
        var accessToken = response.authResponse.accessToken;
        fbSignInCallback(accessToken);
      } else if (response.status === 'not_authorized') {
        var error = messages['notAuth'];
        Materialize.toast(error, 10000);
      } else {
        var error = messages['notLogged'];
        Materialize.toast(error, 10000);
      }
    });
};


var googleSignInCallback = function(authResult){
    if (authResult['code']){
        $.ajax({
            type: 'POST',
            url: '/gconnect?state=' + state,
            processData: false,
            contentType: 'application/json',
            data: authResult['code'],
            success: function(result){
                if(result){
                    var img = result['img'].replace('https','http');
                    hide.login();
                    $('#userImg').attr('src',img);
                    $('#userName').html(result['name']);
                    $('#userEmail').html(result['email']);
                    logged = 1;
                }
                else if (authResult['error']){
                    console.log("Following Error Occured:" + authResult['error']);
                }
                else{
                    console.log('Failed to make connection with server, Please check your internet connection.');
                }
            }
        });
    }
};

var logout = function(){

   if(logged){

    $.ajax({

      type: 'POST',
      url: '/logout',
      processData: false,
      contentType: 'application/json',
      success: function(result){
        if(result['state'] == 'loggedOut'){
          var error = messages['successLogout'];
          Materialize.toast(error, 10000);
          logged = 0;
          hide.user();
        }
        else if (result['state'] == 'notConnected'){
          var error = messages['notConnected'];
          Materialize.toast(error, 10000);
        }
        else if (result['state'] == 'errorRevoke'){
          var error = messages['errorRevoke'];
          Materialize.toast(error, 10000);
        }

      }

    });

   }
   else{

      var error = messages['notConnected'];

      Materialize.toast(error, 10000);
   }

}

gapi.signin.render("googleSignIn", {
              'clientid': '212153352565-f1ti6kcpb65frgfv2uatthhdukdsjtmd.apps.googleusercontent.com',
              'callback': googleSignInCallback,
              'cookiepolicy': 'single_host_origin',
              'requestvisibleactions': 'http://schemas.google.com/AddActivity',
              'scope': 'openid email',
              'redirecturi': 'postmessage',
              'accesstype': 'offline',
              'approvalprompt': 'force'
});

$('#logout').click(function(){
    logout();
});
