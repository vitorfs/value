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

  $(".js-select-all-factors").click(function () {
    var is_checked = $(this).prop("checked");
    $(".factors-checkboxes input[type='checkbox']").each(function () {
      $(this).prop("checked", is_checked);
    });
  });

  $(".factors-checkboxes input[type='checkbox']").click(function () {
    var all_checked = true;
    $(".factors-checkboxes input[type='checkbox']").each(function () {
      if (!$(this).is(":checked")) {
        all_checked = false;
      }
    });
    $(".js-select-all-factors").prop("checked", all_checked);
  });

  // On Page Load
  $(".factors-checkboxes input[type='checkbox']").each(function () {
    if (!$(this).is(":checked")) {
      $(".js-select-all-factors").prop("checked", false);
    }
  });


});
