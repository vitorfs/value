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

      $("#heading-stakeholders .panel-info").append($(".deliverable-manager .avatar").clone());

      $("#collapse-stakeholders .panel-group-stakeholders .panel.panel-success .avatar").each(function () {
        $("#heading-stakeholders .panel-info").append($(this).clone());
      });

      $("#heading-stakeholders .panel-info .avatar").each(function () {
        $(this).css("height", "20px")
               .css("width", "20px")
               .css("font-size", "10px")
               .css("padding-top", "2px")
               .css("margin-right", "0")
               .css("margin-left", "5px");
      });
    }
    else if (target === "collapse-decision-items") {
      $("#heading-decision-items .panel-info .selected-items-count").html($("table.table-decision-items tbody tr td input[type='checkbox']:checked").length);
    }
  });

  $("#new-meeting").submit(function () {
    $(".btn-start-meeting").prop("disabled", true);
    $(".btn-start-meeting").text("Starting the meeting…");
  });

  $("table.table-check-all.table-decision-items").each(function () {
    var totalInputs = $("tbody tr", this).length;
    var totalInputsChecked = $("tbody tr td input[type='checkbox']:checked", this).length;
    if (totalInputs === totalInputsChecked) {
      $("thead tr th input[type='checkbox']", this).prop("checked", true);
    }
  });

});
