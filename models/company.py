## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = "res.company"
    pickingconsignation_id = fields.Many2one('stock.picking.type', 'Ubicación')
    suplier_id = fields.Many2one('res.partner', string='Proveedor')
    companyconsignation_id = fields.Many2one('res.company', string='Compañia')
