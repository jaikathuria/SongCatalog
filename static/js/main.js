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
    "successLogout": "User Successfully Logged Out"
};

$('.button-collapse').sideNav({

      menuWidth: 240, // Default is 240

      edge: 'left', // Choose the horizontal origin

      closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor

      draggable: true // Choose whether you can drag to open on touch screens
    }
  );

$(document).ready(function(){
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
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


 });

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

      },
      error: function(er){
          console.log(er['state']);
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
