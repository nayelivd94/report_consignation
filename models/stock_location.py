## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

class StockLOcation(models.Model):
    _inherit = "stock.location"
    is_consignation = fields.Boolean(string="Es Consignacion", default=False)
    supplier_id = fields.Many2one('res.partner', 'Proveedor de consignación',  domain="[('supplier','=',True)]")
    picking_type_id = fields.Many2one('stock.picking.type', 'Entrega para Consignación')
    det_address_id = fields.Many2one('res.partner', 'Dirección para consignación')
class purchaseOrder(models.Model):
    _inherit='purchase.order'
    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To', states=READONLY_STATES, required=True,help="This will determine picking type of incoming shipment")