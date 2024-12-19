odoo.define('website_mail.follow', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
const { ReCaptcha } = require("google_recaptcha.ReCaptchaV3");
const { _t } = require("web.core");

publicWidget.registry.follow = publicWidget.Widget.extend({
    selector: '#wrapwrap:has(.js_follow)',
    disabledInEditableMode: false,

    /**
     * @constructor
     */
    init() {
        this._super(...arguments);
        this._recaptcha = new ReCaptcha();
    },

    async willStart() {
        return this._recaptcha.loadLibs();
    },

    /**
     * @override
     */
    start: function () {
        var self = this;
        this.isUser = false;
        var $jsFollowEls = this.$el.find('.js_follow');

        var always = function (data) {
            self.isUser = data[0].is_user;
            const $jsFollowToEnable = $jsFollowEls.filter(function () {
                const model = this.dataset.object;
                return model in data[1] && data[1][model].includes(parseInt(this.dataset.id));
            });
            self._toggleSubscription(true, data[0].email, $jsFollowToEnable);
            self._toggleSubscription(false, data[0].email, $jsFollowEls.not($jsFollowToEnable));
            $jsFollowEls.removeClass('d-none');
        };

        const records = {};
        for (const el of $jsFollowEls) {
            const model = el.dataset.object;
            if (!(model in records)) {
                records[model] = [];
            }
            records[model].push(parseInt(el.dataset.id));
        }

        this._rpc({
            route: '/website_mail/is_follower',
            params: {
                records: records,
            },
        }).then(always).guardedCatch(always);

        // not if editable mode to allow designer to edit
        if (!this.editableMode) {
            $('.js_follow > .input-group-append.d-none').removeClass('d-none');
            this.$target.find('.js_follow_btn, .js_unfollow_btn').on('click', function (event) {
                event.preventDefault();
                self._onClick(event);
            });
        }
        return this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Toggles subscription state for every given records.
     *
     * @private
     * @param {boolean} follow
     * @param {string} email
     * @param {jQuery} $jsFollowEls
     */
    _toggleSubscription: function (follow, email, $jsFollowEls) {
        if (follow) {
            this._updateSubscriptionDOM(follow, email, $jsFollowEls);
        } else {
            for (const el of $jsFollowEls) {
                const follow = !email && el.getAttribute('data-unsubscribe');
                this._updateSubscriptionDOM(follow, email, $(el));
            }
        }
    },
    /**
     * Updates subscription DOM for every given records.
     * This should not be called directly, use `_toggleSubscription`.
     *
     * @private
     * @param {boolean} follow
     * @param {string} email
     * @param {jQuery} $jsFollowEls
     */
    _updateSubscriptionDOM: function (follow, email, $jsFollowEls) {
        $jsFollowEls.find('input.js_follow_email')
            .val(email || "")
            .attr("disabled", email && (follow || this.isUser) ? "disabled" : false);
        $jsFollowEls.attr("data-follow", follow ? 'on' : 'off');
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {Event} ev
     */
    async _onClick(ev) {
        var self = this;
        var $jsFollow = $(ev.currentTarget).closest('.js_follow');
        var $email = $jsFollow.find(".js_follow_email");

        if ($email.length && !$email.val().match(/.+@.+/)) {
            $jsFollow.addClass('o_has_error').find('.form-control, .custom-select').addClass('is-invalid');
            return false;
        }
        $jsFollow.removeClass('o_has_error').find('.form-control, .custom-select').removeClass('is-invalid');

        var email = $email.length ? $email.val() : false;
        if (email || this.isUser) {
            const tokenCaptcha = await this._recaptcha.getToken("website_mail_follow");
            const token = tokenCaptcha.token;

            if (tokenCaptcha.error) {
                self.displayNotification({
                    type: "danger",
                    title: _t("Error"),
                    message: tokenCaptcha.error,
                    sticky: true
                });
                return false;
            }
            this._rpc({
                route: '/website_mail/follow',
                params: {
                    'id': +$jsFollow.data('id'),
                    'object': $jsFollow.data('object'),
                    'message_is_follower': $jsFollow.attr("data-follow") || "off",
                    'email': email,
                    'recaptcha_token_response': token,
                },
            }).then(function (follow) {
                self._toggleSubscription(follow, email, $jsFollow);
            });
        }
    },
});
});