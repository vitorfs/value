$(function () {

  $(".js-stakeholders-select-all").click(function () {
    $(".panel-group-stakeholders .panel").each(function () {
      if ($(this).hasClass("panel-default")) {
        $(this).click();
      }
    });
  });

  $(".js-stakeholders-select-none").click(function () {
    $(".panel-group-stakeholders .panel").each(function () {
      if ($(this).hasClass("panel-success")) {
        $(this).click();
      }
    });
  });

  $("main").on("click", "table tbody tr td a.js-remove-row", function (e) {
    $(this).closest("tr").fadeOut(200, function () {
      $(this).remove();
      $("#decision-items-formset").updateFormsetIndex();
    });
  });

  $(".js-add-row").click(function () {
    $(".empty-row").clone().removeClass("empty-row").insertBefore("#decision-items-formset tbody tr.empty-row");
    $("#decision-items-formset").updateFormsetIndex();
  });

/* TODO remove
  var ENTER_KEY = 13;

  var add_item = function (value) {

    if (value.length > 0) {
      var template = [
        "<li class='list-group-item'>",
        "<a href='javascript:void(0);' class='pull-right'><span class='glyphicon glyphicon-remove-sign js-remove-item'></span></a>",
        "<input type='hidden' name='decision_item' value='{value}'>",
        "{value}",
        "</li>"
        ];
      var html = template.join("\n").replace(/{value}/g, value);
      $(".decision-items").prepend(html);
      $(".js-add-item").val("");
    }

  };

  $(".js-add-item").keydown(function (evt) {

    var key_code = evt.which?evt.which:evt.keyCode;

    if (key_code == ENTER_KEY) {
      var value = $(this).val();
      var list = [];

      if (value.indexOf(",") !== -1) {
        list = value.split(",");
      }

      else if (value.indexOf(";") !== -1) {
        list = value.split(";");
      }

      if (list.length > 0) {
        list.forEach(function (e) {
          add_item(e);
        });
      }

      else {
        add_item(value);
      }

      return false;
    }

  });

  $(".js-add-item").keyup(function (evt) {

    var data = $(".js-add-item").val();
    var match = /\r|\n/.exec(data);
    if (match) {
      var list = data.split("\n");
      list.forEach(function (e) {
        add_item(e);
      });
    }

  });

  $(".list-group").on("click", ".js-remove-item", function () {
    $(this).closest("li").remove();
  });
*/

});
