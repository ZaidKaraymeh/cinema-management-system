

document.documentElement.style.setProperty(
  "--nav-height",
  document.getElementById("navbar_cstm").offsetHeight + 20 + "px"
);


var slotsBox = document.getElementById("id_slots");
var opt = document.createElement('option')
opt.value = "---------";
opt.innerHTML = "---------"
slotsBox.appendChild(opt)



async function changeFunc(event) {
  var selectBox = document.getElementById("id_hall");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  
  var date = document.getElementById("id_date");


  var res = await fetch(`http://localhost:8000/slots/${selectedValue}/${date.value}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  })
    .then((response) => response.json())
    .then((json) => {
      var slotsBox = document.getElementById("id_slots");
      slotsBox.innerHTML = ''
      var opt = document.createElement("option");
      opt.value = "---------";
      opt.innerHTML = "---------";
      slotsBox.appendChild(opt);
      for (var propertyName in json){
        var opt = document.createElement('option')
        console.log(typeof propertyName)
        opt.value = propertyName
        opt.innerHTML = json[propertyName]
        slotsBox.appendChild(opt)
      }
    });


}

/* const main = document.getElementsByClassName("body")
main.style.marginTop = document.getElementById("navbar_cstm").offsetHeight + 10;  */