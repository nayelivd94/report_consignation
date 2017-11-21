odoo.define('report_consignation.form', function (require) {
    "use strict";
    var webform = require('web.FormView');
    var common = require('web.form_common');
    var core = require('web.core');
    var crash_manager = require('web.crash_manager');
    var data = require('web.data');
    var Dialog = require('web.Dialog');
    var FormRenderingEngine = require('web.FormRenderingEngine');
    var Model = require('web.DataModel');
    var Pager = require('web.Pager');
    var Sidebar = require('web.Sidebar');
    var utils = require('web.utils');
    var View = require('web.View');
    var _t = core._t;
    var _lt = core._lt;
    var QWeb = core.qweb;
    console.log("HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAA222", webform)
    webform.include({
        on_button_duplicate2: function() {
            var self = this;
            return this.has_been_loaded.then(function() {
                return self.dataset.call('duplicate_consignation', [self.datarecord.id, {}, self.dataset.context]).then(function(new_id) {
                    self.record_created(new_id);
                    self.to_edit_mode();
                });
            });
        },
        /*load_record: function(data) {
            this._super.apply(this, arguments);
            alert(this.$buttons.find('.o_form_button_duplicate'))
            if (this.model!='stock.picking') {
                alert("entro al if")
                alert(this.$buttons)
                this.$buttons.find('.o_form_button_duplicate').css({"display": "none"});
                this.$buttons.find('.o_form_button_duplicate').hide();

            }

           },*/
        render_sidebar: function($node) {

            if (!this.sidebar && this.options.sidebar) {
                this.sidebar = new Sidebar(this, {editable: this.is_action_enabled('edit')});
                if (this.fields_view.toolbar) {
                    this.sidebar.add_toolbar(this.fields_view.toolbar);
                }
                var canDuplicate = this.is_action_enabled('create') && this.is_action_enabled('duplicate');
                var canDuplicate2 = this.is_action_enabled('create') && this.is_action_enabled('duplicate2') && this.model=='stock.picking';
                this.sidebar.add_items('other', _.compact([
                    this.is_action_enabled('delete') && { label: _t('Delete'), callback: this.on_button_delete },
                    canDuplicate && { label: _t('Duplicate'), callback: this.on_button_duplicate },
                    canDuplicate2 && { label: _t('Duplicate consignacion'), callback: this.on_button_duplicate2 }
                ]));

                this.sidebar.appendTo($node);

                // Show or hide the sidebar according to the view mode
                this.toggle_sidebar();
            }
        },

    });



});