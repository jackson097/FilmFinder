// Variables from template
// recent_searches (list of recent searches for user, comma separated)
// movies (list of (movie object, movie, genre) pairs)

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function getSearchHistory() {
    const hr = document.createElement('hr');
    const div = document.createElement('div');
    hr.className = "px-0";
    div.className = "subtitle";
    div.style = "color:#747474 !important;"
    div.innerHTML = "Recent Searches"

    if (recent_searches != "None") {
        var line = document.getElementById("line");
        line.appendChild(hr)

        var subtitle = document.getElementById("subtitle");
        subtitle.appendChild(div);

        var previous = document.getElementById("subtitle_row");
        var entries = recent_searches.split(",");

        length = entries.length;
        if (length > 4) {
            length = 4;
        } 
        
        if (length <= 2) {
            document.getElementById("box").style.height = "65vh";
        } else {
            document.getElementById("box").style.height = "70vh";
        }
        
        for (i = 0; i < length; i++) {
            var entry_div = document.createElement('div');
            var entry_col = document.createElement('div');
            var link = document.createElement('a');
            
            entry_div.className = "row";
            entry_col.className = "col-12 select"
            link.className = "entry"

            link.innerHTML = entries[i];

            insertAfter(previous, entry_div);
            entry_div.appendChild(entry_col);
            entry_col.appendChild(link);

            previous = entry_div;
        }
    }
}

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
