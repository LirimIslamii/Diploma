"use strict";

var KTSignupGeneral = (function () {
    var form;
    var submitButton;
    var validator;
    var passwordMeter;

    var handleForm = function () {
        var validator = FormValidation.formValidation(form, {
            fields: {
                'first-name': {
                    validators: {
                        notEmpty: {
                            message: '<strong class="d-none"></strong>'
                        }
                    }
                },
                'last-name': {
                    validators: {
                        notEmpty: {
                            message: '<strong class="d-none"></strong>'
                        }
                    }
                },
                username: {
                    validators: {
                        notEmpty: {
                            message: '<strong class="d-none"></strong>'
                        }
                    }
                },
                email: {
                    validators: {
                        regexp: {
                            regexp: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                            message: '<strong class="fw-bold">Emaili nuk është i vlefshëm</strong>'
                        },
                        notEmpty: {
                            message: '<strong class="d-none"></strong>'
                        }
                    }
                },
                password1: {
                    validators: {
                        callback: {
                            message: '<strong class="d-none"></strong>',
                            callback: function (input) {
                                var value = input.value;
                                if (value === '') {
                                    return {
                                        valid: false,
                                        message: '<strong class="d-none"></strong>'
                                    };
                                } else if (!validatePassword(value)) {
                                    return {
                                        valid: false,
                                        message: '<strong class="fw-bold">Ju lutemi shkruani fjalëkalimin e vlefshëm</strong>'
                                    };
                                }
                                return true;
                            }
                        }
                    }
                },
                password2: {
                    validators: {
                        notEmpty: {
                            message: '<strong class="fw-bold">Kërkohet konfirmimi i fjalëkalimit</strong>'
                        },
                        identical: {
                            compare: function () {
                                return form.querySelector('[name="password1"]').value;
                            },
                            message: '<strong class="fw-bold">Fjalëkalimet nuk janë të njëjta</strong>'
                        }
                    }
                },
                toc: {
                    validators: {
                        notEmpty: {
                            message: '<strong class="fw-bold">Ju duhet të pranoni termat dhe kushtet</strong>'
                        }
                    }
                }
            },
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                bootstrap: new FormValidation.plugins.Bootstrap5({
                    rowSelector: '.fv-row',
                    eleInvalidClass: 'is-invalid',
                    eleValidClass: 'is-valid'
                })
            }
        });

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
                            window.location.href = redirectUrl;
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

    var validatePassword = function () {
        return passwordMeter ? passwordMeter.getScore() > 50 : false;
    };

    return {
        init: function () {
            form = document.querySelector('#kt_sign_up_form');
            submitButton = document.querySelector('#kt_sign_up_submit');
            passwordMeter = KTPasswordMeter.getInstance(form.querySelector('[data-kt-password-meter="true"]'));
            handleForm();
        }
    };
})();

KTUtil.onDOMContentLoaded(function () {
    KTSignupGeneral.init();
});
