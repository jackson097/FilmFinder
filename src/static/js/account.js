function edit(button, input) {
    button.addEventListener("click", function() {
        if (button.innerHTML == "Edit") {
            input.disabled = false;
            button.innerHTML ="Done";
        } else {
            input.disabled = true;
            button.innerHTML ="Edit";
        }
    });
}

function getImgOrientation(img) {
    var direction; 
    
    if (img.naturalWidth > img.naturalHeight) {
        direction = 'landscape';
    } else if (img.naturalWidth < img.naturalHeight) {
        direction = 'portrait';
    } else {
        direction = 'even';
    }
    
    return direction;
}

var profile_pic = document.getElementById('profile_pic')
var direction = getImgOrientation(profile_pic);

if (direction == "portrait" || direction == "even") {
    profile_pic.style.width = "100px";
} else {
    profile_pic.style.width = "200px";
}

edit(document.getElementById("edit_name"), document.getElementById("full_name_box"))
edit(document.getElementById("edit_email"), document.getElementById("email_box"))