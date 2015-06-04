$(function () {

  $("#table-decision-items").tablesorter({ headers: { 0: { sorter: false }}});

  $("#table-decision-items tbody tr td:not(:first-child)").click(function (e) {
    e.stopPropagation();
    location.href = $(this).closest("tr").attr("data-href");
  });


  $(".js-delete-selected").click(function () {
    $("#id_action").val("delete_selected");
    var can_submit = false;
    $("table tbody tr td input[type='checkbox']").each(function () {
      if ($(this).is(":checked")) {
        can_submit = true;
        return;
      }
    });
    if (can_submit) {
      $(this).closest("form").submit();
    }
    else {
      toastr.warning("Decision items must be selected in order to perform actions on them.");
    }
  });

});
