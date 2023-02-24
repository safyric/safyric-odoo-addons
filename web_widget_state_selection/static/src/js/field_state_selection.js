odoo.define('web_widget_state_selection.state_selection2', function (require) {
    "use strict";
    
    
    var core = require('web.core');
    var BasicFields = require('web.basic_fields');
    
    var qweb = core.qweb;
    
    var StateSelectionWidget2 = BasicFields.StateSelectionWidget.include({
        
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
        
        /**
        * Prepares the state values to be rendered using the FormSelection.Items template.
        *
        * @override
        */
        _prepareDropdownValues: function () {
            var self = this;
            var _data = [];
            var current_stage_id = self.recordData.stage_id && self.recordData.stage_id[0];
            var stage_data = {
                id: current_stage_id,
                legend_normal: this.recordData.legend_normal || undefined,
                legend_in_progress : this.recordData.legend_in_progress || undefined,
                legend_blocked : this.recordData.legend_blocked || undefined,
                legend_done: this.recordData.legend_done || undefined,
            };
            _.map(this.field.selection || [], function (selection_item) {
                var value = {
                    'name': selection_item[0],
                    'tooltip': selection_item[1],
                };
                if (selection_item[0] === 'normal') {
                    value.state_name = stage_data.legend_normal ? stage_data.legend_normal : selection_item[1];
                } else if (selection_item[0] === 'done') {
                    value.state_class = 'o_status_green';
                    value.state_name = stage_data.legend_done ? stage_data.legend_done : selection_item[1];                
                } else if (selection_item[0] === 'in_progress') {
                    value.state_class = 'o_status_blue';
                    value.state_name = stage_data.legend_in_progress ? stage_data.legend_in_progress : selection_item[1];
                } else if (selection_item[0] === 'warning') {
                    value.state_class = 'o_status_yellow';
                    value.state_name = stage_data.legend_warning ? stage_data.legend_warning : selection_item[1];
                    
                } else {
                    value.state_class = 'o_status_red';
                    value.state_name = stage_data.legend_blocked ? stage_data.legend_blocked : selection_item[1];
                }
                _data.push(value);
            });
            return _data;
        },
        
        /**
        * This widget uses the FormSelection template but needs to customize it a bit.
        *
        * @private
        * @override
        */
        _render: function () {
            var self = this;
            var states = this._prepareDropdownValues();
            // Adapt "FormSelection"
            // Like priority, default on the first possible value if no value is given.
            var currentState = _.findWhere(states, {name: self.value}) || states[0];
            this.$('.o_status')
                .removeClass('o_status_red o_status_green o_status_blue o_status_warning')
                .addClass(currentState.state_class)
                .prop('special_click', true)
                .parent().attr('title', currentState.state_name)
                .attr('aria-label', self.string + ": " + currentState.state_name);
            
            // Render "FormSelection.Items" and move it into "FormSelection"
            var $items = $(qweb.render('FormSelection.items', {
                states: _.without(states, currentState)
            }));
            var $dropdown = this.$('.dropdown-menu');
            $dropdown.children().remove(); // remove old items
            $items.appendTo($dropdown);
        },

    });

});

