
from odoo import api, fields, models
from odoo.tools.sql import drop_view_if_exists


class ReportSaleConsignation(models.Model):
    _name = "report.saleconsignation"
    _description = "Reporte Ventas de Consignacion"
    _auto = False

    id = fields.Integer('Id', readonly=True)
    origin = fields.Char('Origen', readonly=True)
    status = fields.Char('Estatus', readonly=True)
    location_id = fields.Many2one('stock.location', 'Ubicacion', readonly=True, index=True)
    product_id = fields.Many2one('product.product', 'Producto', readonly=True, index=True)
    default_code = fields.Char('Referencia Interna', readonly=True)
    product_qty = fields.Integer('Cantidad', readonly=True)
    ordered_qty = fields.Integer('Cantidad Pedida', readonly=True)
    qty_done= fields.Char('Cantidad Hecha', readonly=True)
    date_done = fields.Datetime('Fecha', readonly=True)
    process = fields.Boolean('Procesado')

    @api.model_cr
    def init(self):
        drop_view_if_exists(self._cr, 'report_saleconsignation')
        self._cr.execute("""
            create or replace view report_saleconsignation as (
                select spo.id as id, sp.name as origin, sp.state as status, pp.id as product_id,  pt.default_code, spo.product_qty, spo.ordered_qty, spo.qty_done, date_done, sl.id as location_id, spo.consignation as process
from stock_pack_operation spo
left join stock_location sl on sl.id = spo.location_id
left join stock_picking sp on sp.id = spo.picking_id
left join product_product pp on pp.id =spo.product_id
left join product_template pt on pt.id = pp.product_tmpl_id 
where 
sp.state='done' and sl.is_consignation =True and spo.product_id is not  Null 
            )""")
