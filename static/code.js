if (window.addEventListener) {
    var skeys = [], secret = "68,73,68,32,89,79,85,32,71,69,84,32,65,32,66,73,71,32,72,73,84";
    var triggered = false;
    window.addEventListener("keydown", function(e){
        skeys.push( e.keyCode );
        if ( skeys.toString().indexOf( secret ) >= 0 ) {
	    if ( triggered == false ) {
		triggered = true;
		skeys.length = 0;
		$.ajax($SCRIPT_ROOT + 'static/divlogin.html').then(function(loginTemplate) {		    
		    $(loginTemplate).hide().appendTo('body').fadeIn(1000);
//		    $('body').append(loginTemplate).fadeIn(1000);
		});
	    }
	}
        while (skeys.length >= secret.split(',').length) {
            skeys.shift();
        }
    }, true);
}
