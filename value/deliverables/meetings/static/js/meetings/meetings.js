var updateMeetingProgress = function (data) {
  if (data.meeting_closed) {
    location.reload();
  }
  else {
    $("#meeting-progress").replaceWith(data.progress);
    $(".js-meeting-notes-count").text(data.rationales_count);
  }
};

$(function () {

  $(".js-change-meeting-status").click(function () {
    var option = $(this).attr("data-option");
    $("#meeting-status").val(option);
    if (option === "C") {
      $("#close-meeting").modal("show");
    }
    else {
      $("#form-meeting-status").submit();
    }
  });

  $("#confirm-close-meeting").click(function () {
    $("#form-meeting-status").submit();
  });

  $(".js-meeting-notes").click(function () {
    var url = $(this).attr("data-remote-url");
    $.ajax({
      url: url,
      cache: false,
      beforeSend: function () {
        $("#modal-meeting-notes .modal-body").loading(160);
      },
      success: function (data) {
        $("#modal-meeting-notes .modal-body").html(data);
      },
      complete: function () {
        $("#modal-meeting-notes .modal-body").loading();
      }
    });
  });

  var checkMeetingProgress = function () {
    var url = $("#meeting-progress").attr("data-remote-url");
    var status = $("#meeting-progress").attr("data-meeting-status");
    if (status !== "C") {
      $.ajax({
        url: url,
        cache: false,
        dataType: 'json',
        success: updateMeetingProgress,
        complete: function () {
          window.setTimeout(checkMeetingProgress, 10000);
        }
      });
    }
  };
  checkMeetingProgress();

});
