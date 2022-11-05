

document.documentElement.style.setProperty(
  "--nav-height",
  document.getElementById("navbar_cstm").offsetHeight + 20 + "px"
);


var slotsBox = document.getElementById("id_slots");
var opt = document.createElement('option')
opt.value = "---------";
opt.innerHTML = "---------"
slotsBox.appendChild(opt)



async function changeFunc(value) {
  var selectBox = document.getElementById("id_hall");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;

  var res = await fetch(`http://localhost:8000/slots/${selectedValue}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  })
    .then((response) => response.json())
    .then((json) => {
      console.log(Object.getOwnPropertyNames(json))
      var slotsBox = document.getElementById("id_slots");
      for (var propertyName in json){
        var opt = document.createElement('option')
        opt.value = propertyName
        opt.innerHTML = json[propertyName]
        slotsBox.appendChild(opt)
      }
      /* let options = json.map(
        (o) => `<option value="${o.id}">${o.name}</option>`
      );
      $("id_slots").append(options); */
    });


}

/* const main = document.getElementsByClassName("body")
main.style.marginTop = document.getElementById("navbar_cstm").offsetHeight + 10;  */