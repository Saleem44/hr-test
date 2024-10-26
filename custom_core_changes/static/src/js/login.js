/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.LoginPage = publicWidget.Widget.extend({
    selector: ".oe_login_form, .oe_signup_form", // disabledInEditableMode: true,
    events: {
        "click .eye-btn":"_viewPassword",
    },
     _viewPassword: function (ev) {
        var input1 = $('.password-input-wrap > #password');
        var input2 = $('.password-input-wrap > #confirm_password');
        if (input1.attr("type") === "password" || input2.attr("type") === "password") {
           input1.attr("type", "text");
           input2.attr("type", "text");
        } else {
          input1.attr("type", "password");
          input2.attr("type", "password");
        }
     },
});
