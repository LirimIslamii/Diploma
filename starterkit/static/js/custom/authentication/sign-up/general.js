"use strict";

var KTSignupGeneral = (function () {
  var form;
  var submitButton;
  var validator;
  var passwordMeter;

  var handleForm = function () {
    var validator = FormValidation.formValidation(form, {
      fields: {
        "first-name": {
          validators: {
            notEmpty: {
              message: '<strong class="d-none"></strong>',
            },
          },
        },
        "last-name": {
          validators: {
            notEmpty: {
              message: '<strong class="d-none"></strong>',
            },
          },
        },
        username: {
          validators: {
            notEmpty: {
              message: '<strong class="d-none"></strong>',
            },
          },
        },
        email: {
          validators: {
            regexp: {
              regexp: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
              message:
                '<strong class="fw-bold">Emaili nuk është i vlefshëm</strong>',
            },
            notEmpty: {
              message: '<strong class="d-none"></strong>',
            },
          },
        },
        password1: {
          validators: {
            callback: {
              message: '<strong class="d-none"></strong>',
              callback: function (input) {
                var value = input.value;
                if (value === "") {
                  return {
                    valid: false,
                    message: '<strong class="d-none"></strong>',
                  };
                } else if (!validatePassword(value)) {
                  return {
                    valid: false,
                    message:
                      '<strong class="fw-bold">Ju lutemi shkruani fjalëkalimin e vlefshëm</strong>',
                  };
                }
                return true;
              },
            },
          },
        },
        toc: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Ju duhet të pranoni termat dhe kushtet</strong>',
            },
          },
        },
      },
      plugins: {
        trigger: new FormValidation.plugins.Trigger(),
        bootstrap: new FormValidation.plugins.Bootstrap5({
          rowSelector: ".fv-row",
          eleInvalidClass: "is-invalid",
          eleValidClass: "is-valid",
        }),
      },
    });

    form.querySelectorAll("input[name=password1]").forEach(function (input) {
      input.addEventListener("input", function () {
        document.querySelectorAll(".custom-input1").forEach(function (element) {
          element.classList.add("is-valid");
        });
      });
    });

    submitButton.addEventListener("click", function (e) {
      e.preventDefault();
      validator.validate().then(function (status) {
        document.querySelectorAll(".custom-input1").forEach(function (element) {
          element.classList.add("is-valid");
        });

        if (status === "Valid") {
          submitButton.setAttribute("data-kt-indicator", "on");
          submitButton.disabled = true;
            
          axios
            .post(
              submitButton.closest("form").getAttribute("action"),
              new FormData(form)
            )
            .then(function (response) {
              submitButton.removeAttribute("data-kt-indicator");
              submitButton.disabled = false;
              location.href = '/'
            })
            .catch(function (error) {
              submitButton.removeAttribute("data-kt-indicator");
              submitButton.disabled = false;
              Swal.fire({
                text: error.response.data.message,
                icon: "warning",
                buttonsStyling: false,
                confirmButtonText: "Provoni përsëri",
                customClass: {
                  confirmButton: "btn btn-primary",
                },
              });
            });
        }
      });
    });
  };

  var validatePassword = function () {
    return passwordMeter ? passwordMeter.getScore() > 50 : false;
  };

  return {
    init: function () {
      form = document.querySelector("#kt_sign_up_form");
      submitButton = document.querySelector("#kt_sign_up_submit");
      passwordMeter = KTPasswordMeter.getInstance(
        form.querySelector('[data-kt-password-meter="true"]')
      );
      handleForm();
    },
  };
})();

KTUtil.onDOMContentLoaded(function () {
  KTSignupGeneral.init();
});
