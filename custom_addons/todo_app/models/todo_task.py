from email.policy import default

from odoo import models, fields, api


class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(srtring='Name')
    due_date = fields.Date(string='Due Date' ,tracking=1)
    description = fields.Text(srtring='Description')
    # (tracking=1) to make this fiels display on the chatter
    assign_to = fields.Many2one('res.partner', string='Assign To', tracking=1)
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='new', string='Status', tracking=1)
