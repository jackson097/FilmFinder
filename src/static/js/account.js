function edit(button, input) {
    button.addEventListener("click", function() {
        if (button.innerHTML == "Edit") {
            input.disabled = false;
            button.innerHTML ="Done";
            
        } else {
            // $.ajax({
            //     type: "POST",
            //     url: "/account/",
            //     data: {
            //         "data": $("#full_name_box").val(),
            //     },
            //     success: function(data){
            //         console.log("success");
            //         console.log(data);
            //     },
            //     failure: function(data){
            //         console.log("failure");
            //         console.log(data);
            //     },
            // });
            document.getElementById("full_name_box").readOnly = true;
            document.getElementById("email_box").readOnly = true;
            button.innerHTML ="Edit";
            button.removeAttribute("type")
            button.setAttribute("type","submit")
            // input.disabled = true;
        }
    });
}

function select(element) {
    if (element.classList.contains("selected")) {
        element.classList.remove("selected")
    } else {
        element.classList.add("selected")
    }
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

function previewFile() {
    var preview = document.getElementById('profile_pic')
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();
  
    direction = getImgOrientation(preview);

    if (direction == "portrait" || direction == "even") {
        profile_pic.style.width = "100px";
    } else {
        profile_pic.style.width = "200px";
    }

    reader.onloadend = function () {
      preview.src = reader.result;
    }
  
    if (file) {
      reader.readAsDataURL(file);
    }   
}

function getGenres() {
    var genres = document.getElementsByClassName('choose_genre selected');

    for (i = 0; i < genres.length; i++) {
        document.getElementById("genre_box").value += genres[i].innerHTML + ",";
    }

    console.log(document.getElementById("genre_box").value)
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

console.log(errors);

if (errors) {
    $(document).ready(function($) {
        $('#passwordModal').modal('show');
    });
}