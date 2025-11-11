# Copyright (C) 2025 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    lims_order_ids = fields.Many2many(
        comodel_name="lims.order",
        relation="lims_order_account_move_rel",
        column1="move_id",
        column2="lims_order_id",
        string="LIMS Orders",
    )
    lims_order_count = fields.Integer(
        compute="_compute_lims_order_count", string="LIMS Orders Count"
    )

    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            # Collect all sale orders related to the created moves
            sale_orders = moves.mapped("line_ids.sale_line_ids.order_id")
            # Fetch all related LIMS orders at once
            lims_orders = self.env["lims.order"].search(
                [("sale_order_id", "in", sale_orders.ids)]
            )
            move.lims_order_ids |= lims_orders
        return moves

    @api.depends("lims_order_ids")
    def _compute_lims_order_count(self):
        for rec in self:
            rec.lims_order_count = len(rec.lims_order_ids)

    def action_open_lims_orders(self):
        self.ensure_one()
        return {
            "name": _("LIMS Orders"),
            "type": "ir.actions.act_window",
            "res_model": "lims.order",
            "view_mode": "list,form",
            "domain": [("id", "in", self.lims_order_ids.ids)],
        }
