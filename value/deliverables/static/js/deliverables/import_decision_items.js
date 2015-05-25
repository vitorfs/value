$(function () {

  $(".js-import-decision-items").click(function () {
    $(this).siblings("input[type='file']").click();
  });

  $("#id_import_decision_items").change(function () {

    var data = new FormData();
    data.append("file", $(this)[0].files[0]);
    data.append("csrfmiddlewaretoken", $(this).attr("data-csrf-token"))

    var url = $(this).attr("data-import-url")

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
        //toastr.success("Success!");
        $("#myModal .modal-body").html(data);
        $("#myModal").modal();
      },
      error: function () {
        toastr.error("Error!");
      },
      complete: function () {
        page_loading();
      }
    });

  });

});
