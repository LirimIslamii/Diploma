"use strict";

var KTSigninGeneral = (function () {
  var form;
  var submitButton;
  var validator;

  var handleValidation = function () {
    validator = FormValidation.formValidation(form, {
      fields: {
        username: {
          validators: {
            notEmpty: {
              message: '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        password: {
          validators: {
            notEmpty: {
              message: '<strong class="fw-bold">Kjo fushë është obligative</strong>',
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
  };

  var handleSubmitDemo = function (e) {
    submitButton.addEventListener("click", function (e) {
      e.preventDefault();
      validator.validate().then(function (status) {
        if (status == "Valid") {
          submitButton.setAttribute("data-kt-indicator", "on");
          submitButton.disabled = true;
          form.submit();
        }
      });
    });
  };

  var handleSubmitAjax = function () {
    submitButton.addEventListener('click', function (e) {
      e.preventDefault();
      validator.validate().then(function (status) {
        if (status === 'Valid') {
          submitButton.setAttribute('data-kt-indicator', 'on');
          submitButton.disabled = true;

          axios.post(submitButton.closest('form').getAttribute('action'), new FormData(form))
            .then(function (response) {
              submitButton.removeAttribute('data-kt-indicator');
              submitButton.disabled = false;
              const redirectUrl = form.getAttribute('data-kt-redirect-url');
              location.href = redirectUrl;
            })
            .catch(function (error) {
              submitButton.removeAttribute('data-kt-indicator');
              submitButton.disabled = false;
              var errorMessage = error.response.data.error;
              Swal.fire({
                text: errorMessage,
                icon: "warning",
                buttonsStyling: false,
                confirmButtonText: "Provoni përsëri",
                customClass: {
                  confirmButton: "btn btn-primary"
                }
              });
            });
        }
      });
    });
  };

  var isValidUrl = function (url) {
    try {
      new URL(url);
      return true;
    } catch (e) {
      return false;
    }
  };

  return {
    init: function () {
      form = document.querySelector("#kt_sign_in_form");
      submitButton = document.querySelector("#kt_sign_in_submit");

      handleValidation();

      if (isValidUrl(submitButton.closest("form").getAttribute("action"))) {
        handleSubmitAjax();
      } else {
        handleSubmitDemo();
      }
    },
  };
})();

KTUtil.onDOMContentLoaded(function () {
  KTSigninGeneral.init();
});
