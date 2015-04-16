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
  });

  $(".js-next-wizard-step").click(function () {
    display_content(FORWARD);
  });

  $(".js-previous-wizard-step").click(function () {
    display_content(BACKWARD);
  });
  
});
