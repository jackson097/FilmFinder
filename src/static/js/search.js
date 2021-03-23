function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    m = checkTime(m);
    var ampm = h >= 12 ? 'PM' : 'AM';
    document.getElementById('time').innerHTML =
    h + ":" + m + " " + ampm
    var t = setTimeout(startTime, 500);
  }

  function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
  }

function getDate() {
    var today = new Date();
    var day = today.getDay();
    var month = today.getMonth();
    var num_day = today.getDate();
    var year = today.getFullYear();

    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    var monthArr = ["January", "February","March", "April", "May", "June", "July", "August", "September", "October", "November","December"];

    document.getElementById('date').innerHTML = 
    days[day] + ", " + monthArr[month] + " " + num_day + " " + year;
}

getDate();
