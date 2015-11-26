$(function () {

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
    var target = e.target.id;

    if (target !== "") {
      $(".panel-info", $(this)).fadeIn();
    }

    if (target === "collapse-basic-data") {

    }
    else if (target === "collapse-stakeholders") {
      $("#heading-stakeholders .panel-info").html("");

      $("#heading-stakeholders .panel-info").append('<img src="' + $(".deliverable-manager .img-circle").attr("src").replace("32", "20") + '" alt="' + $(".deliverable-manager .img-circle").attr("alt") + '" class="img-circle" style="margin-left: 5px;">');

      $("#collapse-stakeholders .panel-group-stakeholders .panel.panel-success .img-circle").each(function () {
        $("#heading-stakeholders .panel-info").append('<img src="' + $(this).attr("src").replace("32", "20") + '" alt="' + $(this).attr("alt") + '" class="img-circle" style="margin-left: 5px;">');
      });
    }
    else if (target === "collapse-decision-items") {
      $("#heading-decision-items .panel-info .selected-items-count").html($("#decisionItemsTable tbody tr td input[type='checkbox']:checked").length);
    }
  });

  $("#new-meeting").submit(function () {
    $(".btn-start-meeting").prop("disabled", true);
    $(".btn-start-meeting").text("Starting the meeting…");
  });

});
