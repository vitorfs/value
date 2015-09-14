$(function () {

  var updateSelection = function () {

  };

  $("#available-users").sortable({
    group: { name: "roles", pull: "clone", put: false},
    sort: false
  });

  $(".role").sortable({
    group: "roles",
    onAdd: updateSelection,
    onRemove: updateSelection,
    onEnd: function (evt) {
      
    }
  });

  $("#btn-add-role").click(function () {

    $.ajax({
      url: $("#form-add-role").attr("action"),
      dataType: 'json',
      cache: false,
      beforeSend: function () {
        $("#modal-add-role").modal("show");
      },
      success: function (data) {
        $("#modal-add-role .modal-body").html(data.html);
        $("#modal-add-role").on("shown.bs.modal", function () {
          $("#id_add-name").focus();
        });
      }
    });

  });

  $("#form-add-role").submit(function () {
    $.ajax({
      url: $("#form-add-role").attr("action"),
      data: $("#form-add-role").serialize(),
      type: $("#form-add-role").attr("method"),
      dataType: 'json',
      cache: false,
      success: function(data) {
        if (data.is_valid) {
          location.href = data.redirect_to;
        }
        else {
          $("#modal-add-role .modal-body").html(data.html);
        }
      }
    });
    return false;
  });

});
