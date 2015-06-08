$(function () {

  Sortable.create($("#order-by")[0], { group: "order" });
  Sortable.create($("#columns")[0], { group: "order" });

  Sortable.create($("#column-display-order")[0], { 
    draggable: ".sortable",
    onEnd: function (evt) {
      var value = '';
      $("#column-display-order span").each(function () {
        value += $(this).attr("data-field-name") + ",";
        $(this).attr("data-field-order", $(this).index());
      });
      $("#id_column_display").val(value);
    }
  });

  Sortable.create($("#plain-text-column-order")[0], { draggable: ".sortable" });

  $("#id_orientation").change(function () {
    $("#id_orientation option").each(function () {
      var value = $(this).val();
      $(".entry_per_" + value).hide();
    });
    var value = $(this).val();
    $(".entry_per_" + value).show();
  });

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
