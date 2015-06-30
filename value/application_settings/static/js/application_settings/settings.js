$(function () {

  /*
  Sortable.create($("#order-by")[0], { group: "order" });
  Sortable.create($("#columns")[0], { group: "order" });
  */

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

  /*Sortable.create($("#plain-text-column-order")[0], { draggable: ".sortable" });*/

  $(".js-import-check").click(function () {
    var isActive = $(this).is(":checked");
    var row = $(this).closest("tr");
    $("select", row).prop("disabled", !isActive);    
  });

  $("#id_orientation").change(function () {
    $("#id_orientation option").each(function () {
      var value = $(this).val();
      $(".entry_per_" + value).hide();
    });
    var value = $(this).val();
    $(".entry_per_" + value).show();
  });

  $("[name^='column_is_active']").each(function () {
    var fieldIsntActive = !$(this).is(":checked");
    if (fieldIsntActive) {
      var row = $(this).closest("tr");
      $(".js-control-disable", row).prop("disabled", true);
    }
  });

  $("[name^='column_is_active']").click(function () {
    var isActive = $(this).is(":checked");
    var row = $(this).closest("tr");
    $(".js-control-disable", row).prop("disabled", !isActive);
  });

});
