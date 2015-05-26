$(function () {

  $(".js-stakeholder-selection").click(function () {

    if ($(this).hasClass("bg-success")) {
      $(this).removeClass("bg-success");
      $(this).closest(".panel").addClass("panel-default").removeClass("panel-success");
      $(".glyphicon-ok", this).hide();
      $("[name='stakeholders']", this).prop("checked", false);
    }

    else {
      $(this).addClass("bg-success");
      $(this).closest(".panel").removeClass("panel-default").addClass("panel-success");
      $(".glyphicon-ok", this).show();
      $("[name='stakeholders']", this).prop("checked", true);
    }

  });

  $(".js-stakeholders-select-all").click(function () {
    $(".js-stakeholder-selection").each(function () {
      $(this).addClass("bg-success");
      $(".glyphicon-ok", this).show();
      $("[name='stakeholders']", this).prop("checked", true);
    });
  });

  $(".js-stakeholders-select-none").click(function () {
    $(".js-stakeholder-selection").each(function () {
      $(this).removeClass("bg-success");
      $(".glyphicon-ok", this).hide();
      $("[name='stakeholders']", this).prop("checked", false);
    });
  });

  $.fn.updateFormsetIndex = function () {
    var table = $(this);
    var tableRows = $("tbody tr:not(.empty-row)", this);
    var totalForms = $(tableRows).length;
    $("#id_decision_item-TOTAL_FORMS").val(totalForms);

    $(tableRows).each(function () {
      var rowIndex = $(this).index();
      $("td input", this).each(function () {
        var name = $(this).attr("name");
        $(this).attr("name", name.replace(/-(.*?)-/, "-" + rowIndex + "-"));
        var id = $(this).attr("id");
        $(this).attr("id", id.replace(/-(.*?)-/, "-" + rowIndex + "-"));
      });
    });

  };

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
