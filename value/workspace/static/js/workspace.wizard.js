$(function () {

  var FORWARD = 1;
  var BACKWARD = -1;

  var wizard_steps = ["#basic-data", "#stakeholders", "#decision-making"];
  var current_step_index = 0;

  var wizard_integrity_control = function () {
    if (current_step_index == 0) {
      $(".js-previous-wizard-step").prop("disabled", true);
    }
    else {
      $(".js-previous-wizard-step").prop("disabled", false);
    }

    if (current_step_index == 2) {
      $(".js-submit-wizard").show();
      $(".js-next-wizard-step").hide();
    }
    else {
      $(".js-submit-wizard").hide();
      $(".js-next-wizard-step").show();
    }

  };

  var display_content = function (direction) {
    var last_step;
    var current_step;

    last_step = wizard_steps[current_step_index];
    current_step_index = current_step_index + direction;
    current_step = wizard_steps[current_step_index];

    $(".wizard-content section:visible").fadeOut(400, function () {
      $(".wizard-content section" + current_step).fadeIn(400);
      if (direction == FORWARD) {
        $(".js-wizard-steps button[data-target='" + last_step + "'] .glyphicon").removeClass("hide");
        $(".js-wizard-steps button[data-target='" + current_step + "']").removeClass("btn-default").addClass("btn-primary").prop("disabled", false);
      }
      else if (direction == BACKWARD) {
        $(".js-wizard-steps button[data-target='" + current_step + "'] .glyphicon").addClass("hide");
        $(".js-wizard-steps button[data-target='" + last_step + "']").removeClass("btn-primary").addClass("btn-default").prop("disabled", true);
      }
      wizard_integrity_control();
    });
  };

  $(".js-wizard-steps button").click(function () {
    var target;
    target = $(this).attr("data-target");

    if ("#" + $(".wizard-content section:visible").attr("id") == target) {
      return false;
    }

  });

  $(".js-next-wizard-step").click(function () {
    if (current_step_index == 0) {
      if ($("#id_name").val() === "") {
        $("#id_name").closest(".form-group").addClass("has-error");
        $("#id_name").siblings(".help-block").show();
        return false;
      }
      else {
        $("#id_name").closest(".form-group").removeClass("has-error");
        $("#id_name").siblings(".help-block").hide();
      }
    }
    display_content(FORWARD);
  });

  $(".js-previous-wizard-step").click(function () {
    display_content(BACKWARD);
  });


  $(".js-stakeholder-selection").click(function () {

    if ($(this).hasClass("bg-success")) {
      $(this).removeClass("bg-success");
      $(".glyphicon-ok", this).hide();
      $("[name='stakeholder']", this).prop("checked", false);
    }

    else {
      $(this).addClass("bg-success");
      $(".glyphicon-ok", this).show();
      $("[name='stakeholder']", this).prop("checked", true);
    }

  });

  $(".js-stakeholders-select-all").click(function () {
    $(".js-stakeholder-selection").each(function () {
      $(this).addClass("bg-success");
      $(".glyphicon-ok", this).show();
      $("[name='stakeholder']", this).prop("checked", true);
    });
  });

  $(".js-stakeholders-select-none").click(function () {
    $(".js-stakeholder-selection").each(function () {
      $(this).removeClass("bg-success");
      $(".glyphicon-ok", this).hide();
      $("[name='stakeholder']", this).prop("checked", false);
    });
  });
  
});
