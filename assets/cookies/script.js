console.log('Script.js executed!');


var elt = document.createElement("script");
elt.innerHTML = `window.setTimeout(() => {
    function setCookie(name,value,days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }

    setCookie('ampURL', window.amp.Player.players["vjs_video_3"].cache_.src, 7);
    console.log(window.amp.Player.players["vjs_video_3"].cache_.src);
}, 4000);`;
document.head.appendChild(elt);


















console.log('Script.js executed!');


// var elt = document.createElement("script");
// elt.innerHTML = `window.setTimeout(() => {
//     function setCookie(name,value,days) {
//         var expires = "";
//         if (days) {
//             var date = new Date();
//             date.setTime(date.getTime() + (days*24*60*60*1000));
//             expires = "; expires=" + date.toUTCString();
//         }
//         document.cookie = name + "=" + (value || "")  + expires + "; path=/";
//     }

//     setCookie('ampURL', window.amp.Player.players["vjs_video_3"].cache_.src, 7);
//     console.log(window.amp.Player.players["vjs_video_3"].cache_.src);
// }, 4000);`;
// document.head.appendChild(elt);