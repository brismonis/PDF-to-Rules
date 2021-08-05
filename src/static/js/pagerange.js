function checkrange() {
  var fr = document.getElementById("from").value;
  var to = document.getElementById("to").value;
//   var x=document.forms["myForm"]["age"].value;
  if (fr > to) 
  {
    alert("Invalid Range!");
    return false;
  }
  
}


function showrange() {
    // var x = from.value;
    // var y = to.value;
    // const range = document.getElementById("range")
    // range.classList.remove(".not-visible");
    if(document.getElementById('btnradio2').checked) {
        //Male radio button is checked
        document.getElementById("range").classList.remove("not-visible");
    } else if (document.getElementById('btnradio1').checked) {
        // from.innerText.remove;
        // from.innerHTML.remove;
        // x.remove;
        // y.remove;
        document.getElementById("from").value = null;
        document.getElementById("to").value = null;
        document.getElementById("range").classList.add("not-visible");
    }
    // if (isNaN(x)) {
    //     alert("Must input numbers");
    //     return false;
    // }
    // if (isNaN(y)) {
    //     alert("Must input numbers");
    //     return false;
    // }


}