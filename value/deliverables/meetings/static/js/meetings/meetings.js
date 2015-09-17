$(function () {
  $(".js-decision-item-details").click(function () {
    $(this).tooltip("hide");
    $.ajax({
      url: $(this).attr("data-remote-url"),
      cache: false,
      beforeSend: function () {
        $("#modal-decision-item-details .modal-body").html("");
      },
      success: function (data) {
        $("#modal-decision-item-details .modal-body").html(data);
      }
    });
  });
});
