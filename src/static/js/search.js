// Variables from template
// recent_searches (list of recent searches for user, comma separated)
// movies (list of (movie id, movie, genre) pairs)

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function getSearchHistory() {
    if (recent_searches != "None" && recent_searches != "") {
        document.getElementById('line_element').style.display = "block";

        // Subtitle
        var subtitle = document.getElementById("subtitle");
        subtitle.innerHTML = "Recent Searches";
        subtitle.style = "color:#747474 !important;"
        subtitle.style.fontSize = "12px";
        subtitle.classList.add("pb-2");

        var clearButton = document.getElementById("clear_button");
        clearButton.style = "display: block;";

        var previous = document.getElementById("subtitle_row");
        var entries = recent_searches.split(",").filter(Boolean);

        length = entries.length;
        if (length > 4) {
            length = 4;
        } 

        // // Sizing
        // if(length <= 1) {
        //     document.getElementById("box").style.height = "60vh";
        // } else if (length == 2) {
        //     document.getElementById("box").style.height = "65vh";
        // } else if (length == 3) {
        //     document.getElementById("box").style.height = "70vh";
        // } else if (length == 4) {
        //     document.getElementById("box").style.height = "75vh";
        // }
        
        for (i = 0; i < length; i++) {
            var entryDiv = document.createElement('div');
            var entryCol = document.createElement('div');
            var link = document.createElement('a');
            
            entryDiv.className = "row";
            entryCol.className = "col-12 select"
            link.className = "entry"
            link.id = "entry" + i

            link.innerHTML = entries[i];

            insertAfter(previous, entryDiv);
            entryDiv.appendChild(entryCol);
            entryCol.appendChild(link);

            previous = entryDiv;

            document.getElementById("entry" + i).addEventListener("click", function() {
                document.getElementById("search_query").value = this.innerHTML;
                document.getElementById("enter").click();
            });
        }

        return true;
    } 
    return false;
}

function getTopResults(input, movies_list, genres) {
    // Execute when someone is writing in text field
    input.addEventListener("input", function(e) {
        document.getElementById("line_element").style.display = "block";

        num_results = 0;

        val = this.value;
        var subtitle = document.getElementById("subtitle");
        var previous = document.getElementById("subtitle_row");

        // Change/add subtitle
        subtitle.innerHTML = "Top Results";
        subtitle.style = "color:#747474 !important;"
        subtitle.style.fontSize = "12px"

        // Close any open lists
        closeAllLists();

        // Remove recent searches
        removeRecentSearches();    
        
        subtitle.classList.add("pb-2");
       
        // Nothing typed
        if (!val) {
            return false;
        }

        i = 0;
        while(i < movies_list.length && num_results < 4) {
            if (movies_list[i][1].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                num_results ++;

                // Create link for each matching element
                var div = document.createElement('div');
                var entryDiv = document.createElement('a');
                var entryCol1 = document.createElement('div');
                var entryCol2 = document.createElement('div');
                var genre = document.createElement('div');

                div.className = "delete px-2";
                entryDiv.id = movies_list[i][0];
                entryDiv.className = "row select delete iterate top_result";
                entryCol1.className = "col-4 d-flex align-items-center delete";
                entryCol2.className = "col-8 movie delete ps-0";
                genre.className = "genre px-2 delete";
                entryDiv.href = "movie/" + entryDiv.id;
            
                genre.innerHTML = genres[i];

                // Make matching letters bold
                entryCol2.innerHTML = "<strong>" + movies_list[i][1].substr(0, val.length) + "</strong>";
                entryCol2.innerHTML += movies_list[i][1].substr(val.length);
                entryCol2.innerHTML += "<input type='hidden' value='" + movies_list[i][0] + "'>";

                insertAfter(previous, div);
                div.appendChild(entryDiv);
                entryCol1.appendChild(genre);
                entryDiv.appendChild(entryCol1);
                entryDiv.appendChild(entryCol2);
                
                previous = div;
            } 

            // if (num_results <= 1) {
            //     document.getElementById("box").style.height = "60vh";
            // } else if (num_results == 2) {
            //     document.getElementById("box").style.height = "65vh";
            // } else if (num_results == 3) {
            //     document.getElementById("box").style.height = "70vh";
            // } else if (num_results == 4) {
            //     document.getElementById("box").style.height = "75vh";
            // }

            i++;
        }

        input.addEventListener('input', function(e) {  
            var val = this.value;
    
            if (val == "") {
                if (document.getElementById("subtitle").innerHTML == "Top Results") {
                    searchHistory = getSearchHistory();
                }

                if (!searchHistory) {
                    document.getElementById("line_element").style.display = "none";
                    subtitle.innerHTML = "";
                    // document.getElementById("box").style.height = "55vh";
                    subtitle.classList.remove("pb-2");
                }
            }
        });
    });
}

function closeAllLists() {
    $('.delete').remove();
}

function removeRecentSearches() {
    var subtitle = document.getElementById('subtitle');
    var clearButton = document.getElementById("clear_button");

    $('.entry').parent().parent().remove();
    $('.entry').parent().remove();
    $('.entry').remove();
    clearButton.style = "display: none;";
    subtitle.classList.remove("pb-2");
}

var movie_titles = []
var genres = []

for (i = 0; i < movies.length; i++) {
    movie_titles.push([movies[i][0], movies[i][1]]);
    genres.push(movies[i][2]);
}

getTopResults(document.getElementById("search_query"), movie_titles, genres)

//------------- Don't need anymore, keeping just in case -------------
// function startTime() {
//     var today = new Date();
//     var h = today.getHours();
//     var m = today.getMinutes();
//     m = checkTime(m);
//     var ampm = h >= 12 ? 'PM' : 'AM';
//     document.getElementById('time').innerHTML =
//     h + ":" + m + " " + ampm
//     var t = setTimeout(startTime, 500);
//   }

//   function checkTime(i) {
//     if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
//     return i;
//   }

// function getDate() {
//     var today = new Date();
//     var day = today.getDay();
//     var month = today.getMonth();
//     var num_day = today.getDate();
//     var year = today.getFullYear();

//     var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
//     var monthArr = ["January", "February","March", "April", "May", "June", "July", "August", "September", "October", "November","December"];

//     document.getElementById('date').innerHTML = 
//     days[day] + ", " + monthArr[month] + " " + num_day + " " + year;
// }

// getDate();
