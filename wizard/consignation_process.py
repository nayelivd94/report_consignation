# -*- coding: utf-8 -*-

import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
import logging
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)


class PartnerProcess(models.TransientModel):
    _name = "consignation.process"
    _description = "Procesar"

    @api.model
    def _count(self):
        return len(self._context.get('active_ids', []))
    count = fields.Integer(default=_count, string='# of Rutas')
    date_order =fields.Datetime(string='Order Date', required=True, default=fields.Datetime.now)

    @api.multi
    def process(self):
        check_id = self.env['report.saleconsignation'].browse(self._context.get('active_ids', []))
        total =len(check_id)
        sSelf = self.sudo()
        check=check_id.filtered(lambda i: i.process==False)
        location_obj = sSelf.env['stock.location']
        location_ids = location_obj.search([('is_consignation', '=', True)])
        for loc in location_ids:
            va=check_id.ids
            record= self.env['report.saleconsignation'].search([('location_id','=',loc.id),('id','=',check_id.ids),('process','=',False)])
            if len(record) > 0:
                if loc.supplier_id.id is None or loc.supplier_id.id == False:
                    raise UserError(_("La Ubicación %s no tiene asignada un proveedor de consignación. ")%(loc.name))
                currency = loc.supplier_id.property_product_pricelist.currency_id
                purchase = {
                    'name': sSelf.env['ir.sequence'].next_by_code('purchase.order'),
                    'currency_id': currency.id,
                    'partner_id': loc.supplier_id.id,
                    'company_id': loc.company_id.id,
                    'state': 'draft',
                    'date_order': self.date_order,
                    'date_planned': self.date_order,
                    'picking_type_id': loc.picking_type_id.id,
                    'dest_address_id': loc.det_address_id.id,
                }
                po = sSelf.env['purchase.order'].create(purchase)
                line =[]
                for x in record:
                    product_uom=x.product_id.uom_po_id.id
                    procurement_uom_po_qty = sSelf.env['product.uom']._compute_quantity(x.ordered_qty,product_uom)
                    seller = x.product_id._select_seller(
                        partner_id=loc.supplier_id,
                        quantity=procurement_uom_po_qty,
                        date=po.date_order and po.date_order[:10],
                        uom_id=x.product_id.uom_po_id)

                    taxes = x.product_id.supplier_taxes_id
                    fpos = po.fiscal_position_id
                    taxes_id = fpos.map_tax(taxes) if fpos else taxes
                    if taxes_id:
                        taxes_id = taxes_id.filtered(lambda a: a.company_id.id == loc.company_id.id)

                    price_unit = sSelf.env['account.tax']._fix_tax_included_price(seller.price,
                                                                                 x.product_id.supplier_taxes_id,
                                                                                 taxes_id) if seller else 0.0
                    if price_unit and seller and po.currency_id and seller.currency_id != po.currency_id:
                        price_unit = seller.currency_id.compute(price_unit, po.currency_id)



                    date_planned = sSelf.env['purchase.order.line']._get_date_planned(seller, po=po).strftime(
                        DEFAULT_SERVER_DATETIME_FORMAT)

                    purchase_line = {
                        'order_id': po.id,
                        'product_id': x.product_id.id,
                        'name':x.product_id.name,
                        'product_qty': x.qty_done,
                        'product_uom': x.product_id.uom_po_id.id,
                        'price_unit': price_unit,
                        'currency_id': currency.id,
                        'partner_id': loc.supplier_id.id,
                        'company_id': loc.company_id.id,
                        'state': 'draft',
                        'date_planned': date_planned,
                        'taxes_id': [(6, 0, taxes_id.ids)],


                    }
                    sSelf.env['purchase.order.line'].create(purchase_line)
                    line.append(x.id)
                    pack = sSelf.env['stock.pack.operation'].search([('id','=',x.id)])
                    pack.write({'consignation': True})
                po._amount_all()
                po.write({'origin': line})



