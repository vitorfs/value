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
        toastr.success(data);
        $("#import-modal").modal("hide");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
        $("#import-modal .modal-body").html(jqXHR.responseText);
        toastr.error("An error ocurred while trying to save your data.");
      },
      complete: function (jqXHR, textStatus) {
        page_loading();
      }
    });
  });

});
