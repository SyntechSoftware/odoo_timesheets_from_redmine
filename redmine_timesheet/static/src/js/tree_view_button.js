odoo.define('web.tree_view_button', function (require) {
    "use strict";


    var core = require('web.core');
    var ListView = require('web.ListView');
    var QWeb = core.qweb;
    ListView.include({
        renderButtons: function () {
            // GET BUTTON REFERENCE
            this._super.apply(this, arguments);
            if (this.$buttons) {
                var btn = this.$buttons.find('.o_button_sync')
            }

            // PERFORM THE ACTION
            btn.on('click', this.proxy('do_new_button'))

        },
        do_new_button: function (ev) {
            console.log('3333333');
        },
    });

});