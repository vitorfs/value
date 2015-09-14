$(function () {

  var updateSelection = function (evt) {
    $(".js-btn-remove", evt.item).css("display", "inline");
  };

  $("main").on("click", ".js-btn-remove", function () {
    $(this).closest("li").remove();
  });

  $("#available-users").sortable({
    group: { 
      name: "roles", 
      pull: "clone", 
      put: false
    },
    sort: false
  });

  $(".role").sortable({
    group: "roles",
    onAdd: function (evt) {
      var user = evt.item;
      var ul = $(user).closest("ul");
      var id = $(user).attr("data-user-id");
      var count = 0;
      $("li", ul).each(function () {
        if ($(this).attr("data-user-id") == id) {
          count++;
          if (count > 1) {
            $(this).remove();
          }
        }
      });
      updateSelection(evt);
    },
    onRemove: updateSelection
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
