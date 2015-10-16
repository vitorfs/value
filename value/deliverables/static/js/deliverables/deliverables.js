$(function () {

  $("#addStakeholder").on("show.bs.modal", function () {
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

  $("#formRemoveStakeholder input[name='stakeholders']").change(function () {
    var has_selection = $("#formRemoveStakeholder input[name='stakeholders']:checked").length > 0;
    $("#btn-remove-stakeholders").prop("disabled", !has_selection);
  });

  $("#btn-remove-stakeholders").click(function () {
    $("#formRemoveStakeholder").submit();
  });

});
