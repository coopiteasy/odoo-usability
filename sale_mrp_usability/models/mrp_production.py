# Backport from Odoo v14
# Copyright Odoo SA
# Same licence as Odoo (LGPL)

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_order_count = fields.Integer(
        "Count of Source SO",
        compute='_compute_sale_order_count',
        groups='sales_team.group_sale_salesman')

    @api.depends('move_dest_ids.group_id.sale_id')
    def _compute_sale_order_count(self):
        for production in self:
            production.sale_order_count = len(production.move_dest_ids.mapped('group_id').mapped('sale_id'))

    def action_view_sale_orders(self):
        self.ensure_one()
        sale_order_ids = self.move_dest_ids.mapped('group_id').mapped('sale_id').ids
        action = {
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
        }
        if len(sale_order_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': sale_order_ids[0],
            })
        else:
            action.update({
                'name': _("Sources Sale Orders of %s" % self.name),
                'domain': [('id', 'in', sale_order_ids)],
                'view_mode': 'tree,form',
            })
        return action
