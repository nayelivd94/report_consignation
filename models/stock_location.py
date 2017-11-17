## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)

class StockLOcation(models.Model):
    _inherit = "stock.location"
    is_consignation = fields.Boolean(string="Es Consignacion", default=False)
    supplier_id = fields.Many2one('res.partner', 'Proveedor de consignación',  domain="[('supplier','=',True)]")