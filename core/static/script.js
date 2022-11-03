document.documentElement.style.setProperty(
  "--nav-height",
  document.getElementById("navbar_cstm").offsetHeight
);



const main = document.getElementsByClassName("body")
main.style.marginTop = document.getElementById("navbar_cstm").offsetHeight + 10;