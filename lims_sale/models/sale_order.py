from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    lims_order_count = fields.Integer(
        string="LIMS Orders", compute="_compute_lims_order_count", store=False
    )

    def _compute_lims_order_count(self):
        lims_order_data = self.env["lims.order"].read_group(
            [("sale_order_id", "in", self.ids)], ["sale_order_id"], ["sale_order_id"]
        )
        mapped_data = {
            data["sale_order_id"][0]: data["sale_order_id_count"]
            for data in lims_order_data
        }
        for order in self:
            order.lims_order_count = mapped_data.get(order.id, 0)

    def action_view_lims_orders(self):
        self.ensure_one()
        return {
            "name": "LIMS Orders",
            "type": "ir.actions.act_window",
            "res_model": "lims.order",
            "view_mode": "list,form",
            "domain": [("sale_order_id", "=", self.id)],
            "context": {"default_sale_order_id": self.id},
        }
