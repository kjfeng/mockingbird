
$(document).ready(function() {
  $("#notif-panel").on("click", function(event) {
      // prevents the panel from disappearing when clicked on directly
      event.stopPropagation();

  });
});
