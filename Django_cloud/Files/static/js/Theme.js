function LoadCSS( cssURL ) {
    return new Promise( function( resolve, reject ) {
        let link = document.createElement( 'link' );
        link.rel  = 'stylesheet';
        link.href = cssURL;
        theme = "dark";
        document.head.appendChild( link );
        if (cssURL == "{% static 'style/blue_style.css' %}"){
            theme = "light";
        } else {
            theme = "dark";
        }
        link.onload = function() {
            resolve();
            console.log( 'CSS has loaded!' );
        };
    } );
}
