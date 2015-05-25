$(function () {

  $("#order-by").sortable({
    group: "order",
    store: {
      get: function (sortable) {
        var order = localStorage.getItem(sortable.options.group);
        return order ? order.split('|') : [];
      },
      set: function (sortable) {
        var order = sortable.toArray();
        localStorage.setItem(sortable.options.group, order.join('|'));
      }
    }
  });


  $("#columns").sortable({
    group: "order",
    animation: 150
  });


  $("#column-display-order").sortable({
    draggable: ".sortable"
  });

  $("#plain-text-column-order").sortable({
    draggable: ".sortable"
  });

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
