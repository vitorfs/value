$(function () {

  $(".js-delete-selected").click(function () {
    $("#id_action").val("delete_selected");

    var can_submit = false;

    $("table tbody tr td input[type='checkbox']").each(function () {
      if ($(this).is(":checked")) {
        can_submit = true;
        return;
      }
    });

    if (can_submit) {
      $(this).closest("form").submit();
    }
    else {
      toastr.warning("Groups must be selected in order to perform actions on them.");
    }
  });

  $.fn.fancymultiple = function () {

    var select = $(this);
    
    $(select).css("display", "none");

    var component = [
                      '<div class="row">',
                      '  <div class="col-sm-6">',
                      '    <div class="panel panel-default">',
                      '      <div class="panel-heading">',
                      '        Available stakeholders',
                      '        <span class="glyphicon glyphicon-question-sign help" data-toggle="tooltip" data-placement="top" title="This is the list of available stakeholders. You may choose some by dragging them in the box below and then dropping in the other box."></span>',
                      '      </div>',
                      '      <ul class="list-group sortable" style="min-height: 38px" id="available_stakeholders">{available_stakeholders}</ul>',
                      '    </div>',
                      '  </div>',
                      '  <div class="col-sm-6">',
                      '    <div class="panel panel-primary">',
                      '      <div class="panel-heading">',
                      '        Selected stakeholders',
                      '        <span class="glyphicon glyphicon-question-sign help" data-toggle="tooltip" data-placement="top" title="This is the list of stakeholders whom are members of this group. You may remove some by dragging them in the box below and then dropping in the other box."></span>',
                      '      </div>',
                      '      <ul class="list-group sortable" style="min-height: 38px" id="selected_stakeholders">{selected_stakeholders}</ul>',
                      '    </div>',
                      '  </div>',
                      '</div>'
                    ];

    var template = '<li class="list-group-item" data-user-id="{id}">{name}</li>';

    var available_stakeholders = "";
    var selected_stakeholders = "";

    $("option", select).each(function () {
      if ($(this).prop("selected")) {
        selected_stakeholders += template.replace("{id}", $(this).val()).replace("{name}", $(this).text());
      }
      else {
        available_stakeholders += template.replace("{id}", $(this).val()).replace("{name}", $(this).text());
      }
    });
    
    var html = component.join("\n")
      .replace("{available_stakeholders}", available_stakeholders)
      .replace("{selected_stakeholders}", selected_stakeholders);

    $(select).after(html);

    var updateSelection = function (evt) {
      $("option", select).prop("selected", false);
      $("#selected_stakeholders li").each(function () {
        $("option[value='" + $(this).attr("data-user-id") + "']", select).prop("selected", true);
      });
    };

    $("#available_stakeholders").sortable({
      group: "members"
    });

    $("#selected_stakeholders").sortable({
      group: "members",
      onAdd: updateSelection,
      onRemove: updateSelection
    });

  };

});
