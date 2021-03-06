# Copyright (C) 2019 - TODAY, Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class FSMLocation(models.Model):
    _inherit = 'fsm.location'

    ticket_count = fields.Integer(
        compute='_compute_ticket_count',
        string='# Tickets'
    )

    @api.multi
    def _compute_ticket_count(self):
        for location in self:
            location.ticket_count = self.env['helpdesk.ticket'].search_count(
                [('fsm_location_id', '=', location.id)])

    @api.multi
    def action_view_ticket(self):
        for location in self:
            ticket_ids = self.env['helpdesk.ticket'].search(
                [('fsm_location_id', '=', location.id)])
            action = self.env.ref(
                'helpdesk_fieldservice.action_fsm_location_ticket').read()[0]
            action['context'] = {}
            if len(ticket_ids) == 1:
                action['views'] = [(
                    self.env.ref('helpdesk.helpdesk_ticket_view_form').id,
                    'form')]
                action['res_id'] = ticket_ids.ids[0]
            else:
                action['domain'] = [('id', 'in', ticket_ids.ids)]
            return action
