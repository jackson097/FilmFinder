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
    profile_pic.style.width = "40px";
} else {
    profile_pic.style.width = "80px";
}
console.log(direction);