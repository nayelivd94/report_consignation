## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)

class StockPackOperation(models.Model):
    _inherit = "stock.pack.operation"
    consignation = fields.Boolean(string="Consignacion", default=False)