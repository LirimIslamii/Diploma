"use strict";

var KTSigninGeneral = (function () {
  var form;
  var submitButton;
  var resetButton;
  var validator;

  var handleValidation = function () {
    validator = FormValidation.formValidation(form, {
      fields: {
        learning_rate: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        num_epochs: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        kernel_size: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        optimizer: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        metrics: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        batch_size: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        num_kernels: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        validation_split: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        lr_scheduler_params: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
        early_stopping: {
          validators: {
            notEmpty: {
              message:
                '<strong class="fw-bold">Kjo fushë është obligative</strong>',
            },
          },
        },
      },
      plugins: {
        trigger: new FormValidation.plugins.Trigger(),
        bootstrap: new FormValidation.plugins.Bootstrap5({
          rowSelector: ".form-group",
          eleInvalidClass: "",
          eleValidClass: "",
        }),
      },
    });
  };

  var handleSubmitDemo = function (e) {
    submitButton.addEventListener("click", function (e) {
      e.preventDefault();
      validator.validate().then(function (status) {
        if (status == "Valid") {
          form.submit();
        }
      });
    });
  };

  var handleResetForm = function () {
    resetButton.addEventListener("click", function (e) {
      e.preventDefault();
      form.reset();
      validator.resetForm(true);
      $('.form-select').val(null).trigger('change');
    });
  };

  return {
    init: function () {
      form = document.querySelector("#kt_register");
      submitButton = document.querySelector("#kt_register_submit");
      resetButton = document.querySelector("#reset_button");

      handleValidation();
      handleSubmitDemo();
      handleResetForm();
    },
  };
})();

document.addEventListener("DOMContentLoaded", function () {
  KTSigninGeneral.init();
});
