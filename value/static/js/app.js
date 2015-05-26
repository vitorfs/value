var page_loading = function () {
  if ($("body").hasClass("no-scroll")) {
    $("body").removeClass("no-scroll");
  }
  else {
    $("body").addClass("no-scroll");
  }
  $(".page-loading").toggle();
};

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

$(function () {

  $("[data-toggle='popover']").popover();

  $(".menu-link").bigSlide({
    side: 'right',
    push: '.wrapper, footer',
    menuWidth: '18.6em'
  });

  $("[data-toggle='tooltip']").tooltip();

  $("[data-toggle='popover']").popover();

  toastr.options = {
    "closeButton": true,
    "preventDuplicates": true
  };

  $("input, textarea").attr("autocomplete", "off");

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

});
