"use strict";

var KTSignupGeneral = (function () {
    var form;
    var submitButton;
    var validator;
    var passwordMeter;

    var handleForm = function () {
        validator = FormValidation.formValidation(form, {
            fields: {
                'first-name': {
                    validators: {
                        notEmpty: {
                            message: 'Kjo fushë është obligative'
                        }
                    }
                },
                'last-name': {
                    validators: {
                        notEmpty: {
                            message: 'Kjo fushë është obligative'
                        }
                    }
                },
                username: {
                    validators: {
                        notEmpty: {
                            message: 'Kjo fushë është obligative'
                        }
                    }
                },
                email: {
                    validators: {
                        regexp: {
                            regexp: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                            message: 'Emaili nuk është i vlefshëm'
                        },
                        notEmpty: {
                            message: 'Kjo fushë është obligative'
                        }
                    }
                },
                password1: {
                    validators: {
                        notEmpty: {
                            message: 'Kjo fushë është obligative'
                        },
                        callback: {
                            message: 'Ju lutemi shkruani fjalëkalimin e vlefshëm',
                            callback: function (input) {
                                return input.value.length > 0 && validatePassword();
                            }
                        }
                    }
                },
                password2: {
                    validators: {
                        notEmpty: {
                            message: 'Kërkohet konfirmimi i fjalëkalimit'
                        },
                        identical: {
                            compare: function () {
                                return form.querySelector('[name="password1"]').value;
                            },
                            message: 'Fjalëkalimet nuk janë të njëjta'
                        }
                    }
                },
                toc: {
                    validators: {
                        notEmpty: {
                            message: 'Ju duhet të pranoni termat dhe kushtet'
                        }
                    }
                }
            },
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                bootstrap: new FormValidation.plugins.Bootstrap5({
                    rowSelector: '.fv-row',
                    eleInvalidClass: '',
                    eleValidClass: ''
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
                            Swal.fire({
                                text: "Ju jeni regjistruar me sukses!",
                                icon: "success",
                                buttonsStyling: false,
                                confirmButtonText: "Në rregull!",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            }).then(function (result) {
                                if (result.isConfirmed) {
                                    const redirectUrl = form.getAttribute('data-kt-redirect-url');
                                    location.href = redirectUrl;
                                }
                            });
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
        return passwordMeter.getScore() > 50;
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
