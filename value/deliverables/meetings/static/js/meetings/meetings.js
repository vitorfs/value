$(function () {
  $(document).on("click", ".js-decision-item-details", function () {
    $(this).tooltip("hide");
    var url = $(this).attr("data-remote-url");
    $.ajax({
      url: url,
      cache: false,
      beforeSend: function () {
        $("#modal-decision-item-details .modal-body").html("");
      },
      success: function (data) {
        $("#modal-decision-item-details .modal-body").html(data);
      }
    });
  });

  $(".js-meeting-notes").click(function () {
    var url = $(this).attr("data-remote-url");
    $.ajax({
      url: url,
      cache: false,
      beforeSend: function () {
        $("#modal-meeting-notes .modal-body").html("");
      },
      success: function (data) {
        $("#modal-meeting-notes .modal-body").html(data);
      }
    });
  });
});
