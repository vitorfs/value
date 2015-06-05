$(function () {

  var initializeDecisionItemsTable = function () {
    $("#decision-items-table").tablesorter({ headers: { 0: { sorter: false }}});
    $("#decision-items-table tbody tr td:not(:first-child)").click(function (e) {
      e.stopPropagation();
      location.href = $(this).closest("tr").attr("data-href");
    });
  };

  initializeDecisionItemsTable();

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

  $(".js-confirm-import").click(function () {
    var data = $("#import-decision-items-container :input").serialize();
    var url = $("#import-decision-items-container").attr("data-save-import-url");
    data += "&csrfmiddlewaretoken=" + $("#import-decision-items-container").attr("data-csrf-token");
    $.ajax({
      url: url,
      data: data,
      type: 'post',
      cache: false,
      beforeSend: function (jqXHR, settings) {
        page_loading();
      },
      success: function (data, textStatus, jqXHR) {
        toastr.success("The data were imported successfully!");
        $("#decision-items-table").replaceWith(data);
        initializeDecisionItemsTable();
        initializeCheckAll();
        $("#import-modal").modal("hide");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        if (jqXHR.status === 400) {
          $("#import-modal .modal-body").html(jqXHR.responseText);
          toastr.error("A data validation error ocurred. Please review the highlighted fields.");
        }
        else {
          toastr.error("An error ocurred while trying to save your data.");
        }
      },
      complete: function (jqXHR, textStatus) {
        page_loading();
      }
    });
  });

});
