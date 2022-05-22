function myFunction() {
    var x = document.getElementById("top-nav");
    if (x.className === "navbar") {
      x.className += " responsive";
    } else {
      x.className = "navbar";
    }
  }