function getTimedEvals() {
    var tryoutID = document.getElementById("tryoutid").value;
    var form = document.getElementById("getfileform");
    var downloadlink = "http://localhost:5000/downloadTimedEvals/" + tryoutID;
    form.setAttribute("action", downloadlink);
    form.submit();
}