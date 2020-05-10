function LoadCSS( cssURL ) {
    return new Promise( function( resolve, reject ) {
        let link = document.createElement( 'link' );
        link.rel  = 'stylesheet';
        link.href = cssURL;
        theme = "light";
        document.head.appendChild( link );
        if (theme == "light"){
            theme = "dark";
        } else {
            theme = "light";
        }
        link.onload = function() {
            resolve();
            console.log( 'CSS has loaded!' );
        };
    } );
}
