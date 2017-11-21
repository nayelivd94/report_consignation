# -*- coding: utf-8 -*-
{
    'name': "Reporte de Ventas de Consignación",

    'summary': """
      Reporte de Ventas de Consignación""",

    'description': """
   Reporte de Ventas de Consignación
    """,

    'author': "Nayeli Valencia Díaz",
    'website': "http://www.xmarts.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','stock'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_consignationsale.xml',
        'views/stock_location.xml',
        #'views/consignation_picking.xml',
        'views/form_view.xml',
'views/company.xml',
        'wizard/consignation_process.xml',
    'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}