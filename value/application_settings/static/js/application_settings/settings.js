$(function () {

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
