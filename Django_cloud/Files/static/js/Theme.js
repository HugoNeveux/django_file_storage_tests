function LoadCSS( cssURL ) {
    return new Promise( function( resolve, reject ) {
        let link = document.createElement( 'link' );
        link.rel  = 'stylesheet';
        link.href = cssURL;
        let dark = 0;
        document.head.appendChild( link );
        if (dark == 0){
            dark=1;
        } else {
            dark=0;
        }
        link.onload = function() {
            resolve();
            console.log( 'CSS has loaded!' );
        };
    } );
}
