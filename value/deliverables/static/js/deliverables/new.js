$(function () {

  $(".js-stakeholders-select-all").click(function () {
    $(".panel-group-stakeholders .panel").each(function () {
      if ($(this).hasClass("panel-default")) {
        $(this).click();
      }
    });
  });

  $(".js-stakeholders-select-none").click(function () {
    $(".panel-group-stakeholders .panel").each(function () {
      if ($(this).hasClass("panel-success")) {
        $(this).click();
      }
    });
  });

  $("main").on("click", "table tbody tr td a.js-remove-row", function (e) {
    $(this).closest("tr").fadeOut(200, function () {
      $(this).remove();
      $("#decision-items-formset").updateFormsetIndex();
    });
  });

  $(".js-add-row").click(function () {
    $(".empty-row").clone().removeClass("empty-row").insertBefore("#decision-items-formset tbody tr.empty-row");
    $("#decision-items-formset").updateFormsetIndex();
  });

  $(".js-confirm-import").click(function () {
    var rows = $("#decision-items-import-table tbody tr").clone();
    $("#import-modal").one('hidden.bs.modal', function(e) {
      page_loading();
      $(rows).insertBefore("#decision-items-formset tbody tr.empty-row");
      $("#decision-items-formset").updateFormsetIndex();
      page_loading();
    }).modal("hide");
  });

});
