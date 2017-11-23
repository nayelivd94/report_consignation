## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"
    is_consignation = fields.Boolean(string="es consignacion", default=False)

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
            default['is_consignation'] = True
            #default['company_id'] = self.company_id.companyconsignation_id.id
        ids= super(StockPicking, self).copy(default=default)
        company = self.company_id.companyconsignation_id.id
        stock = self.env['stock.picking'].search([('id', '=', ids.id)])
        stock.write({'company_id': company})
        type=self.env['stock.picking.type']
        pick=stock.picking_type_id
        stock_name= type.search([('id','=',pick.id)])
        nombre =stock_name.sequence_id.next_by_id()
        #stock.write({'name': })
        moves = self.env['stock.move'].search([('picking_id', '=', ids.id)])
        for m in moves:
            m.write({'company_id': company})
        return ids