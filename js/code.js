if true {//(window.addEventListener) {
/*    var skeys = [], secret = "68,73,68,32,89,79,85,32,71,69,84,32,65,32,66,73,71,32,72,73,84";
    var triggered = false;
    window.addEventListener("keydown", function(e){
        skeys.push( e.keyCode );
        if ( skeys.toString().indexOf( secret ) >= 0 ) {
	    if ( triggered == false ) {
		triggered = true;
		skeys.length = 0;
*/		$("#divlogin").load( "template/divlogin.html");
		$("body").append($("#divlogin"));
/*	    } else if (triggered == true) {
		triggered = false;
		$("#divlogin").remove();
	    }
	}
        while (skeys.length >= secret.split(',').length) {
            skeys.shift();
        }
    }, true);
*/}
