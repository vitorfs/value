$(function () {

  $("form").submit(function () {
    var form = $(this);
    $.ajax({
      url: $(form).attr("action"),
      data: $(form).serialize(),
      type: $(form).attr("method"),
      cache: false,
      statusCode: {
        200: function () {

        }
      },
      beforeSend: function (jqXHR, settings) {
        $("button[type='submit']", form).prop("disabled", true);
        $("button[type='submit']", form).text("Saving changes…");
      },
      success: function (data, textStatus, jqXHR) {
        toastr.success(data);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        toastr.error("An error ocurred while trying to save your data.");
      },
      complete: function (jqXHR, textStatus) {
        $("button[type='submit']", form).prop("disabled", false);
        $("button[type='submit']", form).text("Save changes");
      }
    });
    return false;
  });

});
