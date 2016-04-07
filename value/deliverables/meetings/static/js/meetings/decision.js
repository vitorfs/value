$(function () {
  $("#table-final-decision").tablesorter();

  $("#form-final-decision").change(function () {
    var form = $(this);
    $.ajax({
      url: $(form).attr("action"),
      type: $(form).attr("method"),
      data: $(form).serialize(),
      beforeSend: function () {

      },
      success: function () {
        $("#table-final-decision tbody tr").removeClass();
      },
      error: function (xhr) {
        var ids = xhr.responseJSON;
        $("#table-final-decision tbody tr").removeClass();
        ids.forEach(function (value) {
          $("[data-item-id='" + value + "']").addClass("bg-danger");
        });
        toastr.error("Provide a valid meeting ranking. Only decimal value allowed.");
      },
      complete: function () {
        $("#table-final-decision [name$='meeting_ranking']").each(function () {
          var ranking = $(this).val();
          $(this).siblings("span").text(ranking);
        });
        $("#table-final-decision").trigger("update");
      }
    })
  });


  $(".js-rationale").popover({
    html: true,
    content: function () {
      var rationale = $(this).attr("data-rationale");
      var id = uuid();
      var template = $('#rationale-template').html();
      var rendered = Mustache.render(template, {
        'rationale': rationale,
        'id': id
      });
      return rendered;
    }
  });

  $(".js-rationale").on("shown.bs.popover", function () {
    var popover = $(this).siblings(".popover");
    if ($("textarea", popover).text().length === 0 && !$("textarea", popover).prop("readonly")) {
      $("textarea", popover).focus();
    }
  });


  $(document).on("click", ".js-save-rationale", function () {
    var container = $(this).closest(".popover");
    var btn = $(this);

    var url = $(this).closest("td").find(".js-rationale").attr("data-save-url");
    var rationale = $(".final-decision-rationale", container).val();

    rationale = rationale.trim();

    $.ajax({
      url: url,
      type: 'post',
      cache: false,
      data: {
        'csrfmiddlewaretoken': getCSRF(),
        'text': rationale
      },
      beforeSend: function (jqXHR, settings) {
        $(btn).prop("disabled", true);
        $(btn).text("Saving…");
      },
      success: function (data, textStatus, jqXHR) {
        toastr.success("Rationale saved successfully!");
        $(container).siblings(".js-rationale").attr("data-rationale", rationale);
        if (rationale.length > 0) {
          $(container).siblings(".js-rationale").removeClass("btn-default").addClass("btn-primary");
        }
        else {
          $(container).siblings(".js-rationale").removeClass("btn-primary").addClass("btn-default");
        }
        $(container).popover("hide");
        updateMeetingProgress(data);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        toastr.error(jqXHR.responseText);
      },
      complete: function (jqXHR, textStatus) {
        $(btn).prop("disabled", false);
        $(btn).text("Save");
      }
    });

  });

});
