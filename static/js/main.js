
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

 });