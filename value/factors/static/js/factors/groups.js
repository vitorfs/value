$(function () {

  $("#new-group").on("shown.bs.modal", function () {
    $("#id_name").focus();
  });

  $("#modal-edit-group").on("shown.bs.modal", function () {
    $("#modal-edit-group input[type='text']").focus();
  });

  $("#btn-save-group-edit").click(function () {
    $("#modal-edit-group form").submit();
  });

  $(".js-confirm-group-deletion").click(function () {
    var group_id = $(this).attr("data-group-id");
    var group_name = $(this).attr("data-group-name");
    $("#form-delete-group [name='group']").val(group_id)
    $("#form-delete-group .group-name").text(group_name);
    $("#delete-group").modal("show");
  });

  $(".js-edit-group").click(function () {
    var url = $(this).attr("data-group-edit-url");
    var form = $("#form-edit-group");
    $.ajax({
      url: url,
      type: 'get',
      cache: false,
      beforeSend: function () {
        $("#modal-edit-group").modal("show");
      },
      success: function (data) {
        $("#modal-edit-group .modal-body").html(data);
      }
    });
  });

  var updateSelection = function (evt) {
    var factor_id = $(evt.item).attr("data-factor-id");
    var group = $(evt.item).closest(".list-group");
    var group_id = $(group).attr("data-group-id");

    $("#id_group").val(group_id);
    $("#id_factor").val(factor_id);

    var form = $("#form-add-factor-group");
    $.ajax({
      url: $(form).attr("action"),
      type: $(form).attr("method"),
      data: $(form).serialize(),
      cache: false
    });
  };

  $("#available-factors").sortable({
    group: "factors"
  });

  $(".factors-group").sortable({
    group: "factors",
    onAdd: updateSelection,
    onRemove: updateSelection
  });

});