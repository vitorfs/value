$(function () {
  $(".js-decision-item-details").click(function () {
    $.ajax({
      url: $(this).attr("data-remote-url"),
      cache: false,
      beforeSend: function () {
        $("#modal-decision-item-details").modal('show');
        $("#modal-decision-item-details .modal-body").html("");
      },
      success: function (data) {
        $("#modal-decision-item-details .modal-body").html(data);
      }
    });
  });
});
