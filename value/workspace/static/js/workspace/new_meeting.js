$(function () {

  $("#starting_date").datetimepicker({
    format: "DD/MM/YYYY HH:mm",
    defaultDate: moment()
  });

  $("#ending_date").datetimepicker({
    format: "DD/MM/YYYY HH:mm",
    defaultDate: moment().add(1, 'hours')
  });

  $(".sortable").tablesorter({ headers: { 0: { sorter: false }}});

  $(".panel").on("show.bs.collapse", function (e) {
    $(".panel-info", $(this)).fadeOut();
  });

  $(".panel").on("hide.bs.collapse", function (e) {
    $(".panel-info", $(this)).fadeIn();
  });

});
