(function ($) {
  "use strict";
  $(function () {
    var body = $("body");
    var sidebar = $(".sidebar");

    $(".horizontal-menu .nav li a").each(function () {
      var $this = $(this);
      addActiveClass($this);
    });
    var holidayDates = []
    if(undefined !== $('#holiday_list').val() && ''!= $('#holiday_list').val()) {
      holidayDates = $('#holiday_list').val().split(',').map(function(dateStr) {
        var parts = dateStr.split('-');
        return new Date(parts[0], parts[1] - 1, parts[2]);
      });
    }

    flatpickr('.datepicker', {
      enableTime: true,
      dateFormat: "Y-m-d H:i",
      minDate: "today",
      disable: [
        function(date) {
            return (date.getDay() === 0 || date.getDay() === 6);
        },
        ...holidayDates
      ],
    });

    //Close other submenu in sidebar on opening any
    sidebar.on("show.bs.collapse", ".collapse", function () {
      sidebar.find(".collapse.show").collapse("hide");
    });

    $('[data-toggle="minimize"]').on("click", function () {
      if (
        body.hasClass("sidebar-toggle-display") ||
        body.hasClass("sidebar-absolute")
      ) {
        body.toggleClass("sidebar-hidden");
      } else {
        body.toggleClass("sidebar-icon-only");
      }
    });

    //checkbox and radios
    $(".form-check label,.form-radio label").append(
      '<i class="input-helper"></i>'
    );

    //Horizontal menu in mobile
    $('[data-toggle="horizontal-menu-toggle"]').on("click", function () {
      $(".horizontal-menu .bottom-navbar").toggleClass("header-toggled");
    });
    // Horizontal menu navigation in mobile menu on click
    var navItemClicked = $(".horizontal-menu .page-navigation >.nav-item");
    navItemClicked.on("click", function (event) {
      if (window.matchMedia("(max-width: 991px)").matches) {
        if (!$(this).hasClass("show-submenu")) {
          navItemClicked.removeClass("show-submenu");
        }
        $(this).toggleClass("show-submenu");
      }
    });

    $(window).scroll(function () {
      if (window.matchMedia("(min-width: 992px)").matches) {
        var header = $(".horizontal-menu");
        if ($(window).scrollTop() >= 70) {
          $(header).addClass("fixed-on-scroll");
        } else {
          $(header).removeClass("fixed-on-scroll");
        }
      }
    });

    $('#id_meeting').change(function() {
      var meetingId = $(this).val();
      var url = $('#get_url').val();
      var csrftoken = $('[name="csrfmiddlewaretoken"]').attr('value');
      
      $.ajax({
          url: url,
          type: 'GET',
          data: {
              'meeting_id': meetingId,
          },
          dataType: 'json',
          success: function(data) {
            $('#id_meeting_date').datepicker('setDate', data.meeting_date);
          },
          error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error fetching date:', textStatus, errorThrown);
          }
      });
    });

    $('#mark_present').click(function(){
      moveOptions('#id_absent_users', '#id_present_users');
      updateHiddenFields();
    })
    
    $('#mark_absent').on('click', function() {
      moveOptions('#id_present_users', '#id_absent_users');
      updateHiddenFields();
    });
    
    $('#id_absent_users').on('dblclick', 'option:selected', function() {
      moveOptions('#id_absent_users', '#id_present_users');
      updateHiddenFields();
    });

    $('#id_present_users').on('dblclick', 'option:selected', function() {
      moveOptions('#id_present_users', '#id_absent_users');
      updateHiddenFields();
    });

    $('#mark_all_present').on('click', function() {
      moveAllOptions('#id_absent_users', '#id_present_users');
      updateHiddenFields();
    });

    $('#mark_all_absent').on('click', function() {
      moveAllOptions('#id_present_users', '#id_absent_users');
      updateHiddenFields();
    });

    function moveOptions(fromId, toId) {
      const $fromSelect = $(fromId);
      const $toSelect = $(toId);

      $fromSelect.find('option:selected').each(function() {
          $(this).remove().appendTo($toSelect);
      });
    }

    function moveAllOptions(fromId, toId) {
      const $fromSelect = $(fromId);
      const $toSelect = $(toId);

      $fromSelect.find('option').each(function() {
          $(this).remove().appendTo($toSelect);
      });
    }

    function updateHiddenFields() {
      const unselectedUsers = $('#id_absent_users option').map(function() {
        return $(this).val();
      }).get();
    
      const selectedUsers = $('#id_present_users option').map(function() {
        return $(this).val();
      }).get();
    
      $('#hidden_unselected_users').val(unselectedUsers.join(','));
      $('#hidden_selected_users').val(selectedUsers.join(','));
    }
  });

  init_datatables();
  //init_datePickers();
  init_deleteModal();
  init_menu();
  has_value_inputs();
  init_response();
  responseModal();
  meetings_list_redirect();
  view_response();
  __agenda__();
  __action__item__();

  alert_message_hide_show();
})(jQuery);

function init_datatables() {
  if ($(".dataTable").length) {
    $(function () {
      $(".dataTable").DataTable();
    });
  }
}

function init_datePickers() {
  if ($(".datepicker").length) {
    const datepicker = $(".datepicker").datepicker({
      format: "dd-mm-yyyy",
      autoclose: true,
      todayHighlight: true,
    });

    datepicker.on("changeDate", function () {
      const input = $(this);
      if (input.val()) {
        input.addClass("has-value");
      } else {
        input.removeClass("has-value");
      }
    });

    $(".datepicker_wrapper .input-group-append").on("click", function (e) {
      e.preventDefault();
      $(this).siblings("input")[0].focus();
    });
  }
}

function init_deleteModal() {
  if ($(".delete_meeting").length) {
    $(document).on("click", ".delete_meeting", function (e) {
      e.preventDefault();

      let href = $(this).data("href");
      $("#deleteModal").find("form").attr("action", href);
      $("#deleteModal").modal("show");
    });
  }
}

function init_menu() {
  $(".sidebar ul.nav li").each(function (e, t) {
    let target_a = $(t).find("a");
    if ($(target_a).hasClass("active")) {
      $(target_a).parents("div.collapse").addClass("show");
      if ($(target_a).parents("div.collapse").parent(".nav-item").length) {
        $(target_a)
          .parents("div.collapse")
          .parent(".nav-item")
          .addClass("active");
      } else {
        $(target_a).parent(".nav-item").addClass("active");
      }

      $(target_a)
        .parents("div.collapse")
        .parent(".nav-item")
        .find(".nav-link .has_child")
        .addClass("rotate");
    }
  });
}

function has_value_inputs() {
  const inputs = $(".form-floating .form-control");

  inputs.each(function () {
    const input = $(this);
    input.on("input", function () {
      if (input.val()) {
        input.addClass("has-value");
      } else {
        input.removeClass("has-value");
      }
    });

    if (input.val()) {
      input.addClass("has-value");
    }
  });
}

function init_response() {
  $(".add-response").on("click", function () {
    var actionItemId = $(this).data("id");
    $("#responseForm").attr(
      "action",
      "/meetings/action-item/responses/" + actionItemId + "/add"
    );
  });
}

function responseModal() {
  $("#responseModal").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var actionItem = button.data("action-item"); // Extract info from data-* attributes
    var modal = $(this);
    console.log(actionItem);
    // Update the modal's content with the action item value
    modal.find("#id_action_item").val(actionItem);
  });
}

function meetings_list_redirect() {
  if ($(".meeting_list_").length) {
    $(document).on("change", ".meeting_list_", function (e) {
      e.preventDefault();
      let meeting_id = $(this).val();
      window.location.href = "/meetings/" + meeting_id + "/action-items";
    });
  }
}

function view_response() {
  $(document).on("click", ".view_response", function (event) {
    event.preventDefault();
    var url = $(this).attr("href");

    $.get(url, function (data) {
      $("#responsesModal .modal-content").html(
        $(data).find(".modal-content").html()
      );
      $("#responsesModal").modal("show");
    });
  });
}

function __agenda__() {
  if ($(".add_agenda_btn").length) {
    $(".add_agenda_btn").on("click", function (e) {
      e.preventDefault();
      $(this).find("i").toggleClass("fa-minus");
      $(".add_agenda_form").slideToggle();
    });

    __edit__agenda__();
  }

  function __edit__agenda__() {
    if ($(".edit_agenda_btn").length) {
      $(".edit_agenda_form").on("click", function (e) {
        e.stopPropagation();
      });

      $(".close_agenda").on("click", function (e) {
        e.stopPropagation();
        $(this).parents(".edit_agenda_form").hide();
        $(this)
          .parents(".edit_agenda_form")
          .next(".agenda_title")
          .slideToggle();
      });

      $(".edit_agenda_btn").on("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        $($(this).parent().siblings(".edit_agenda_form")[0]).slideToggle();
        $(this).parent().hide();
      });

      $(".update_agenda").on("click", function (e) {
        let $this = $(this);
        $(".alert").remove();
        e.preventDefault();
        agenda_id = $(this).data("agenda_id");
        let form = $(this).parents(".edit_agenda_form").serialize();

        var formArray = $(this).parents(".edit_agenda_form").serializeArray();
        var formObject = {};
        $.each(formArray, function (i, field) {
          formObject[field.name] = field.value;
        });

        $.post(
          "/meetings/agenda/" + formObject.agenda_id + "/update/",
          form
        ).done(function (res) {
          if (res.success) {
            $("body .main-panel .content-wrapper").append(
              '<div class="alert alert-success alert-dismissible fade show">Agenda Updated Successfully<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
            );

            $this
              .parents("form")
              .next(".agenda_title")
              .text(formObject.agenda_title);
          } else {
            $("body .main-panel .content-wrapper").append(
              '<div class="alert alert-danger alert-dismissible fade show">Something went wrong!<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
            );
          }
          $this.parents("form").hide();
          $this.parents("form").next(".agenda_title").show();
        });
      });
    }
  }
}

function __action__item__() {
  if ($(".btn.add_action_item").length) {
    $(".btn.add_action_item").on("click", function (e) {
      e.preventDefault();
      $(this).find("i").toggleClass("fa-minus");
      $(this).parent().next(".add_action_item_form").slideToggle();
    });
  }
}
function alert_message_hide_show() {
  $(".alert").each(function () {
    var alert = $(this);
    setTimeout(function () {
      alert.removeClass("show").addClass("hide");
      setTimeout(function () {
        alert.remove();
      }, 500); // Wait for the hide transition to finish before removing
    }, 3000);
  });
}

function toggleLoginForm() {
  const form = document.getElementById("custom-login-form");
  const content = form.querySelector(".hidden-form-content");
  const arrowIcon = document.getElementById("toggle-arrow").querySelector("i");

  if (form.classList.contains("open")) {
    form.style.height = `${content.offsetHeight}px`; // Set height to current height for smooth transition
    window.requestAnimationFrame(() => {
      form.style.height = "0";
    });
    form.classList.remove("open");
    arrowIcon.classList.remove("fa-caret-up");
    arrowIcon.classList.add("fa-caret-down");
  } else {
    form.style.height = "0";
    form.classList.add("open");
    window.requestAnimationFrame(() => {
      form.style.height = `${content.offsetHeight}px`;
    });
    arrowIcon.classList.remove("fa-caret-down");
    arrowIcon.classList.add("fa-caret-up");
  }
}

function alert_message_hide_show() {
  $(".alert").each(function () {
    var alert = $(this);
    setTimeout(function () {
      alert.removeClass("show").addClass("hide");
      setTimeout(function () {
        alert.remove();
      }, 500); // Wait for the hide transition to finish before removing
    }, 3000);
  });
}

function toggleLoginForm() {
  const form = document.getElementById("custom-login-form");
  const content = form.querySelector(".hidden-form-content");
  const arrowIcon = document.getElementById("toggle-arrow").querySelector("i");

  if (form.classList.contains("open")) {
    form.style.height = `${content.offsetHeight}px`; // Set height to current height for smooth transition
    window.requestAnimationFrame(() => {
      form.style.height = "0";
    });
    form.classList.remove("open");
    arrowIcon.classList.remove("fa-caret-up");
    arrowIcon.classList.add("fa-caret-down");
  } else {
    form.style.height = "0";
    form.classList.add("open");
    window.requestAnimationFrame(() => {
      form.style.height = `${content.offsetHeight}px`;
    });
    arrowIcon.classList.remove("fa-caret-down");
    arrowIcon.classList.add("fa-caret-up");
  }
}
