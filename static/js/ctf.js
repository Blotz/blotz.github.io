// Simple script for generating new flags
// var message = "";
// var salt = CryptoJS.lib.WordArray.random(128 / 8).toString();

// var hash = CryptoJS.PBKDF2(message, salt, {
//     keySize:128 / 32,
//     iterations: 100_000,
// });

// var ctf = hash + salt;
// alert(ctf);

function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

function hashFlag(flag, ctf) {
    var ctf_salt = ctf.substring(32,64);

    var hash = CryptoJS.PBKDF2(flag, ctf_salt, {
        keySize:128 / 32,
        iterations: 100_000,
    });

    return hash + ctf_salt;
}

function ctfVerify() {
    // var flag = document.getElementById("flag").value;
    var flag = document.ctfForm.flag.value;

    if( flag != "") {
        // alert(flag);
        readTextFile("/ctf/ctf_hash.json", function(text){
            var data = JSON.parse(text); //parse JSON
            // console.log(data);

            // check each flag
            for (const ctf in data) {
                // console.log(ctf);
                var flag_hash = hashFlag(flag, ctf);

                if (ctf == flag_hash) {
                    return alert("Found flag \"" + data[ctf]['name'] + "\"!\n" + data[ctf]['description']);
                }
            }
            alert("Not a flag :(");
        });
    }
    document.ctfForm.flag.focus();
}