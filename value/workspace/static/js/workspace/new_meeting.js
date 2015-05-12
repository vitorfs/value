$(function () {

  $("#starting_date").datetimepicker({
    format: "DD/MM/YYYY HH:mm",
    defaultDate: moment()
  });

  $("#ending_date").datetimepicker({
    format: "DD/MM/YYYY HH:mm",
    defaultDate: moment().add(1, 'hours')
  });

});
