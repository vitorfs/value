$(function () {

  $(".js-import-decision-items").click(function () {
    $(this).siblings("input[type='file']").click();
  });

  $("#id_import_decision_items").change(function () {

    if (Modernizr.xhr2) {
      var url = $(this).attr("data-import-url")
      var data = new FormData();
      data.append("file", $(this)[0].files[0]);
      data.append("csrfmiddlewaretoken", $(this).attr("data-csrf-token"));

      $.ajax({
        url: url,
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        type: 'post',
        beforeSend: function () {
          page_loading();
        },
        success: function (data) {
          $("#import-modal .modal-body").html(data);
          $("#import-modal").modal("show");
        },
        error: function (jqXHR) {
          toastr.warning(jqXHR.responseText);
        },
        complete: function () {
          page_loading();
        }
      });
    }

  });

  $("#import-modal").on("hidden.bs.modal", function (e) {
    $("#import-modal .modal-body").html("");
  });

});
