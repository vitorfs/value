$(function () {

  $("#add-stakeholder").on("show.bs.modal", function () {
    var url = $(this).attr("data-url");
    var modal = $(this);
    $.ajax({
      url: url,
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(".modal-body", modal).html("<div class='loading-container' style='margin: 60px 0 20px'></div>");
        $(".modal-body .loading-container", modal).loading();
      },
      success: function (data) {
        $(".modal-body", modal).html(data);
      }
    });
  });

  $("#form-remove-stakeholder input[name='stakeholders']").change(function () {
    var has_selection = $("#form-remove-stakeholder input[name='stakeholders']:checked").length > 0;
    $("#btn-remove-stakeholders").prop("disabled", !has_selection);
  });

  $("#btn-confirm-remove-stakeholders").click(function () {
    var clear_data = $("#confirm-clear-data").is(":checked");
    if (clear_data) {
      $("#form-remove-stakeholder input[name='clear_user_related_data']").val("True");
      $(this).text("Please wait, this can take a few minutes…")
    }
    $(this).prop("disabled", true);
    $("#form-remove-stakeholder").submit();
  });

});
