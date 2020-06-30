window.onload = function() {
    var nav = document.getElementById('nav'),
    anchor = nav.getElementsByTagName('a'),
    current = window.location.pathname.split('/')[1];
    for (var i = 0; i < anchor.length; i++) {vb
        if(anchor[i].getAttribute("href") == current) {
            anchor[i].className = "pagename current";
        }
    }
}