$(function () {

  $(".deliverable-stakeholders .panel-group-stakeholders .panel").click();

  $("#starting_date").datetimepicker({
    format: "DD/MM/YYYY HH:mm"
  });

  $(".table-sortable").tablesorter({ headers: { 0: { sorter: false }}});

  $(".panel").on("show.bs.collapse", function (e) {
    if (e.target.id !== "") {
      $(".panel-info", $(this)).fadeOut();
    }
  });

  $(".panel").on("hide.bs.collapse", function (e) {
    if (e.target.id !== "") {
      $(".panel-info", $(this)).fadeIn();
    }
  });

});
