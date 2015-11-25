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

});
