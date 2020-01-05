
$(document).ready(function() {
  $("#notif-panel").on("click", function(event) {
      // prevents the panel from disappearing when clicked on directly
      event.stopPropagation();

  });

  $(".close").on("click", function(event) {
      // prevents the panel from disappearing when clicked on directly
      $(".survey-card").css("display", "none");
      $(".modal-backdrop").css("display", "none");
  });
});
