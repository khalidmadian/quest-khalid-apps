from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PlayGroundCraft(models.Model):
    _name = 'playground.craft'
    _description = 'Playground Craft'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=1)
    governorate = fields.Char(string='Governorate', required=1)
    owner_id = fields.Many2one('res.partner', string='Owner')
    owner_phone = fields.Char(string='Owner Phone', related='owner_id.phone', readonly=0)
    length = fields.Float(string='Length (L)')
    width = fields.Float(string='Width (W)')
    area = fields.Char(string='Area', compute='area_compute_field')  # area in sq meters
    social = fields.Text(string='Social')
    expected_rented_date = fields.Date(string='Expected Rented Date')
    is_late = fields.Boolean(string='Is Late', readonly=True)
    description = fields.Text(string='Description')
    rent_price = fields.Float(string='Rent Price', tracking=1)
    coffe_shop = fields.Boolean(string='Coffe Shop')
    restaurant = fields.Boolean(string='Restaurant')
    shower = fields.Boolean(string='Shower')
    active = fields.Boolean(default=True)
    playground_floor = fields.Selection([
        ('grass', 'Grass'),
        ('sand', 'Sand'),
        ('asphalt', 'Asphalt'),
        ('artificial_turf', 'Artificial Turf'),
        ('concrete', 'Concrete'),
        ('indoor_synthetic_flooring', 'Indoor Synthetic Flooring')

    ])
    state = fields.Selection([
        ('under_construction', 'Under construction'),
        ('ready', 'Ready'),
        ('rented', 'Rented'),
        ('closed', 'closed')

    ], default='under_construction')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name should be unique')
    ]

    @api.constrains('rent_price')
    def _check_rent_price_greater_50(self):
        if self.rent_price < 50:
            raise ValidationError('Rent price should be greater than 50')

    def action_under_construction(self):
        for rec in self:
            rec.state = 'under_construction'
            print('inside action_under_construction')

    def action_ready(self):
        for rec in self:
            rec.state = 'ready'
            print('inside ready')

    def action_rented(self):
        for rec in self:
            rec.state = 'rented'
            print('inside rented')

    @api.depends('length', 'width')
    def area_compute_field(self):
        for rec in self:
            print("inside area_compute_field")
            rec.area = rec.length * rec.width

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    def check_expected_rented_date(self):
        playground_id = self.search([])
        for rec in playground_id:
            if rec.expected_rented_date and rec.expected_rented_date < fields.Date.today():
                rec.is_late = True

    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(PlayGroundCraft, self).create(vals)
    #     print("inside create")
    #     return res

    # def _search(self, args, offset=0, limit=None, order=None, count=False):
    #     res = super(PlayGroundCraft, self)._search(args, offset=0, limit=None, order=None, count=None)
    #     print("inside search")
    #     return res
    #
    # def write(self, vals):
    #     res = super(PlayGroundCraft, self).write(vals)
    #     print("inside write")
    #     return res
    #
    # def unlink(self):
    #     res = super(PlayGroundCraft, self).unlink()
    #     print("inside unlink")
    #     return res
