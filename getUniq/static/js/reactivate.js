function disableSubmitBtn() {
   btn = document.getElementById("submit-btn")
   btn.classList.remove("btn-blue");
   btn.firstChild.data = "Submitting...";
   btn.disabled = true;
}
