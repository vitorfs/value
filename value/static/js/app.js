var page_loading = function () {
  if ($("body").hasClass("no-scroll")) {
    $("body").removeClass("no-scroll");
  }
  else {
    $("body").addClass("no-scroll");
  }
  $(".page-loading").toggle();
};

var uuid = function () {
  var _uuid ='xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
      return v.toString(16);
  });
  return _uuid;
};

var getCSRF = function () {
  return $("meta[name='csrf']").attr("content");
}

$.fn.loading = function () {
  if ($(this).hasClass("loading")) {
    $(this).find(".block-spinner").remove();
    $(this).removeClass("loading");
  }
  else {
    var center = (parseInt($(this).css("height")) / 2) - 40;
    $(this).addClass("loading");
    $(this).html("<div class='block-spinner' style='margin-top: " + center + "px;'></div>");
  }
};

$.fn.updateFormsetIndex = function () {
  var table = $(this);
  var tableRows = $("tbody tr:not(.empty-row)", this);
  var totalForms = $(tableRows).length;
  $("[id$='TOTAL_FORMS']").val(totalForms);

  $(tableRows).each(function () {
    var rowIndex = $(this).index();
    $("td input, td select", this).each(function () {
      var name = $(this).attr("name");
      $(this).attr("name", name.replace(/-(.*?)-/, "-" + rowIndex + "-"));
      var id = $(this).attr("id");
      $(this).attr("id", id.replace(/-(.*?)-/, "-" + rowIndex + "-"));
    });
  });

};

$.fn.selectizeUsers = function (options, maxItems) {

  maxItems = typeof maxItems !== 'undefined' ? maxItems : 1;

  $(this).selectize({
    maxItems: maxItems,
    valueField: 'pk',
    labelField: 'name',
    searchField: ['name'],
    options: options,
    render: {
      item: function (item, escape) {
        return "<div>" + item.name + "</div>"
      },
      option: function (item, escape) {
        return "<div><img src='" + item.img + "' alt='" + item.name + "' class='img-circle' style='margin-right: 10px;'><span style='line-height: 20px;'>" + item.name + "</span></div>";
      }
    }
  });

};

var colorLuminance = function (hex, lum) {
  hex = String(hex).replace(/[^0-9a-f]/gi, '');
  if (hex.length < 6) {
    hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
  }
  lum = lum || 0;
  var rgb = "#", c, i;
  for (i = 0; i < 3; i++) {
    c = parseInt(hex.substr(i*2,2), 16);
    c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
    rgb += ("00"+c).substr(c.length);
  }
  return rgb;
};

var initializeCheckAll = function () {
  $("table.table-check-all thead tr th input[type='checkbox']").click(function () {
    var is_checked = $(this).is(":checked");
    var table = $(this).closest("table");
    if (is_checked) {
      $("tbody tr td input[type='checkbox']", table).prop("checked", true);
    }
    else {
      $("tbody tr td input[type='checkbox']", table).prop("checked", false);
    }
  });

  $("table.table-check-all").on("click", "input[type='checkbox']", function () {
    var table = $(this).closest("table");
    var all_checked_flag = true;
    var checked_count = 0;
    $("tbody tr td input[type='checkbox']", table).each(function () {
      if ($(this).is(":checked")) {
        checked_count = checked_count + 1;
      }
      else {
        all_checked_flag = false;
      }
    });
    $("tfoot tr td span.count", table).text(checked_count);
    $("thead tr th input[type='checkbox']", table).prop("checked", all_checked_flag);
  });
};

$(function () {

  initializeCheckAll();

  /*
  $(".menu-link").bigSlide({
    side: 'right',
    push: '.wrapper, footer',
    menuWidth: '18.6em'
  });
  */

  $("[data-toggle='tooltip']").tooltip();

  toastr.options = {
    "closeButton": true,
    "preventDuplicates": true
  };

  $("main").on("click", ".panel-group-stakeholders.selectable .panel", function () {
    if ($(this).hasClass("panel-success")) {
      $(".panel-body", this).removeClass("text-success bg-success");
      $(this).removeClass("panel-success").addClass("panel-default");
      $(".panel-body small", this).removeClass("text-success");
      $(".panel-action-icon .glyphicon-ok", this).hide();
      $("[name='stakeholders']", this).prop("checked", false);
    }
    else {
      $(".panel-body", this).addClass("bg-success text-success");
      $(this).removeClass("panel-default").addClass("panel-success");
      $(".panel-body small", this).addClass("text-success");
      $(".panel-action-icon .glyphicon-ok", this).show();
      $("[name='stakeholders']", this).prop("checked", true);
    }
  });

  $(".panel-group-stakeholders.removeable .panel").hover(function () {
    $(this).removeClass("panel-default").addClass("panel-danger");
    $(".panel-body", this).addClass("bg-danger text-danger");
    $(".panel-body small", this).addClass("text-danger");
    $(".panel-action-icon .glyphicon-remove", this).show();
  }, function () {
    $(this).removeClass("panel-danger").addClass("panel-default");
    $(".panel-body", this).removeClass("bg-danger text-danger");
    $(".panel-body small", this).removeClass("text-danger");
    $(".panel-action-icon .glyphicon-remove", this).hide();
  });

  $(".table-clickable-row tbody tr").click(function (e) {
    e.stopPropagation();
    location.href = $(this).attr("data-href");
  });

  /* Active/Inactive grid buttons */

  $(".js-toggle-active").click(function () {
    var component = $(this);
    var icon = $(".glyphicon", this);
    var is_active = $(this).attr("data-is-active") === "True";
    $.ajax({
      url: 'active/',
      type: 'post',
      data: {
        'id': $(component).attr("data-id"),
        'csrfmiddlewaretoken': getCSRF()
      },
      success: function () {
        toastr.success("Changes successfully saved!");
        if (is_active) {
          $(icon).removeClass().addClass("glyphicon glyphicon-remove-sign text-danger")
          $(component).attr("data-is-active", "False");
        }
        else {
          $(icon).removeClass().addClass("glyphicon glyphicon-ok-sign text-success")
          $(component).attr("data-is-active", "True");
        }
      },
      error: function () {
        toastr.error("An unexpected error ocurred. This might be caused by a network failure. Please try again later.");
      }
    });
  });

  /* Stackable Modal */

  $('[data-toggle="modal"]').on('click', function(){
    var $btn = $(this);
    var currentDialog = $btn.closest('.modal-dialog'),
    targetDialog = $($btn.attr('data-target'));;
    if (!currentDialog.length)
      return;
    targetDialog.data('previous-dialog', currentDialog);
    currentDialog.addClass('aside');
    var stackedDialogCount = $('.modal.in .modal-dialog.aside').length;
    if (stackedDialogCount <= 5){
      currentDialog.addClass('aside-' + stackedDialogCount);
    }
  });

  $('.modal').on('hide.bs.modal', function(){
    var $dialog = $(this);  
    var previousDialog = $dialog.data('previous-dialog');
    if (previousDialog){
      previousDialog.removeClass('aside');
      $dialog.data('previous-dialog', undefined);
    }
  });

});
