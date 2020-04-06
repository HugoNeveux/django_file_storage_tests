function LoadCSS( cssURL ) {
    return new Promise( function( resolve, reject ) {
        var link = document.createElement( 'link' );
        link.rel  = 'stylesheet';
        link.href = cssURL;
        document.head.appendChild( link );
        link.onload = function() {
            resolve();
            console.log( 'CSS has loaded!' );
        };
    } );
}
