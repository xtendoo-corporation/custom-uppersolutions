from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    is_hour_category = fields.Boolean(string="Categoría Horas")
    is_travel_category = fields.Boolean(string="Categoría desplazamiento")

