function validateForm() {
    var x = document. forms["Form"]["question"].value;
    var a = document.forms["Form"]["answer1"].value;
    var b = document.forms["Form"]["answer2"].value;
    var c = document.forms["Form"]["answer3"].value;
    var d = document.forms["Form"]["answer4"].value;
    if ((x == null || x == "") || (a == null || a == "") || (b == null || b == "")) {
      alert("Please fill out at least the question and answers 1 & 2");
      return false;
    }
  }
