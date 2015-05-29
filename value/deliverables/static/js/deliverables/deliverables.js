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

  $("#formRemoveStakeholder .panel").click(function () {

    var form = $(this).closest("form");
    var panel = $(this);
    var user_id = $("[name='stakeholders']", this).val();
    var csrf_token = $("[name='csrfmiddlewaretoken']", form).val();
    
    $.ajax({
      url: $(form).attr("action"),
      type: 'post',
      cache: false,
      data: {
        'csrfmiddlewaretoken': csrf_token,
        'user_id': user_id
      },
      success: function (data) {
        $(panel).fadeOut(400, function () {
          $(this).remove();
        });
        toastr.success(data);
      }
    });

  });

});
