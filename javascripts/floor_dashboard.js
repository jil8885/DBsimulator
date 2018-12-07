function getQueryStringObject() {
    let a = window.location.search.substr(1).split('&');
    if (a === "") return {};
    let b = {};
    for (let i = 0; i < a.length; ++i) {
        let p = a[i].split('=', 2);
        if (p.length == 1)
            b[p[0]] = "";
        else
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
    }
    return b;
}

function draw() {
    let x = Math.floor(Math.random() * 400) + 1;
    let canvas = document.getElementById("canvas");
    if (canvas.getContext) {
        canvas.style.left = x + "px";
        canvas.style.position = "absolute";
        setTimeout(function () {
            draw();
        }, 1500);
    }
}

window.onload = function () {
    draw();
}