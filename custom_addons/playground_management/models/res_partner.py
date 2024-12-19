from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    playground_name = fields.Many2one('playground.craft', string="playground's", help="Playground Name... ")

