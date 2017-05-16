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

  $(".js-sync-jira").click(function () {
    var btn = $(this);
    var url = btn.attr("data-remote");
    $.ajax({
      url: url,
      cache: false,
      beforeSend: function () {
        btn.prop("disabled", true);
        $(".btn-state-default", btn).hide();
        $(".btn-state-loading", btn).show();
      },
      success: function (data) {
        toastr.success("JIRA synced with success!");
      },
      error: function (xhr) {
        $("#jira-error-body").text(xhr.responseText);
        $("#modal-jira-error").modal();
      },
      complete: function () {
        btn.prop("disabled", false);
        $(".btn-state-default", btn).show();
        $(".btn-state-loading", btn).hide();
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
