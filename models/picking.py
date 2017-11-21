## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def copy(self, default=None):
        if default is None:
            default={}
        default['partner_id'] = 7
        default['company_id'] = 1
        return super(StockPicking, self).copy(default=default)

    @api.multi
    @api.returns('self', lambda value: value.id)
    def duplicate_consignation(self, default=None):
        if default is None:
            default={}
        id=self.company_id
        if self.company_id.suplier_id.id is None or self.company_id.suplier_id.id is False or self.company_id.pickingconsignation_id.id is None or self.company_id.pickingconsignation_id.id is False:
            raise UserError(_("Configure la duplicidad de consignación en su compañia"))
        else:
            default['partner_id'] = self.company_id.suplier_id.id
            default['picking_type_id'] = self.company_id.pickingconsignation_id.id
            default['company_id'] = self.company_id.companyconsignation_id.id
        ids=super(StockPicking, self).copy(default=default)
        company=self.company_id.companyconsignation_id.id
        moves = self.env['stock.move'].search([('picking_id','=',self.id)])
        for m in moves:
            m.write({'company_id': company})
        return ids