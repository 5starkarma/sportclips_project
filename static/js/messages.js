var messages = document.getElementById("main-messages");
setTimeout(function() {
  if (messages) {
    messages.classList.add('boop');
  }
}, 100);
setTimeout(function() {
  if (messages) {
    messages.classList.add('hide');
  }
}, 5000);