# Copyright (C) 2025 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    lims_laboratory_ids = fields.Many2many(
        "res.partner",
        "res_users_lims_laboratory_rel",
        "user_id",
        "partner_id",
        string="LIMS Laboratories",
        domain="[('is_laboratory', '=', True)]",
        help=(
            "Laboratories this user can access. "
            "Used by record rules to filter LIMS records by laboratory."
        ),
    )
