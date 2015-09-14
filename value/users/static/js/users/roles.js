$(function () {

  $("main").on("click", ".js-btn-remove", function () {
    var li = $(this).closest("li");
    var user = $(li).attr("data-user-id");
    var role = $(li).closest("ul").attr("data-role-id");
    removeUserFromRole(user, role);
    $(li).remove();
  });

  $("#available-users").sortable({
    group: { 
      name: "roles", 
      pull: "clone", 
      put: false
    },
    sort: false
  });

  var removeUserFromRole = function (user, role) {
    var form = $("#form-remove-user-role");
    $("#id_user_remove").val(user);
    $("#id_role_remove").val(role);
    $.ajax({
      url: $(form).attr("action"),
      type: $(form).attr("method"),
      data: $(form).serialize(),
      success: function () {

      }
    });
  };

  $(".role").sortable({
    group: "roles",
    onAdd: function (evt) {
      var user = evt.item;
      var ul = $(user).closest("ul");
      var id = $(user).attr("data-user-id");
      var count = 0;
      var is_duplicated = false;
      $("li", ul).each(function () {
        if ($(this).attr("data-user-id") == id) {
          count++;
          is_duplicated = count > 1;
          if (is_duplicated) {
            $(this).remove();
          }
        }
      });

      if (!is_duplicated) {
        var form = $("#form-add-user-role");
        $("#id_user").val($(user).attr("data-user-id"));
        $("#id_role").val($(ul).attr("data-role-id"));
        $.ajax({
          url: $(form).attr("action"),
          type: $(form).attr("method"),
          data: $(form).serialize(),
          success: function () {

          }
        });
      }

      $(".js-btn-remove", evt.item).css("display", "inline");
    },
    onRemove: function (evt) {
      var user = $(evt.item).attr("data-user-id");
      var role = $(evt.from).attr("data-role-id");
      removeUserFromRole(user, role);
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
