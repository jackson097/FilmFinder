function select(element) {
    if (element.classList.contains("selected")) {
        element.classList.remove("selected")
    } else {
        element.classList.add("selected")
    }
}

function getGenres() {
    var genres = document.getElementsByClassName('choose_genre selected');

    for (i = 0; i < genres.length; i++) {
        document.getElementById("genre_box").value += genres[i].innerHTML + ",";
    }

    console.log(document.getElementById("genre_box").value)
}