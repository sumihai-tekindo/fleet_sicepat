from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
global invoice,account_id,invoice_id


class fleet_vehicle_log_contract(osv.osv):
	_inherit = 'fleet.vehicle.log.contract'

	_columns = {
		#'account_id' :fields.many2one('account.account', 'Account Supplier Invoice',required=True),
		'product_id' :fields.many2one('product.product', 'Product', required=True),
		'department_id' :fields.many2one('account.invoice.department', 'Department',required=True),
		'invoice_id':fields.boolean(default=False, copy=False),
	}
	###ADD queue to supplier invoice
	def compute_rent(self, cr, uid, ids, context=None):
		record = self.browse(cr, uid, ids)
		account_id =0
		amount=0
		#if record.invoice_id:
		sewa=True
		start_date=record.start_date
		end_date1=record.expiration_date
		vals={'type':'in_invoice','partner_id':record.insurer_id.id,'account_id':record.insurer_id.property_account_payable.id,'currency_id':record.insurer_id.company_id.currency_id.id,'department_id':10,'date_invoice':record.date,'sewa':True,'date_start':start_date,'date_end':end_date1}
		account=self.pool['account.invoice'].create(cr, uid, vals,context=context) 
		product=record.product_id
		cost_subtype_id=record.cost_subtype_id.id
		amount=record.amount
		
		print "-------------=======amount==========--",amount,
		print "-------------=======start_date==========--",start_date,
		print "-------------=======end_date==========--",end_date1,
		
		rent_vals={'product_id':product.id, 'invoice_id':account, 'name':record.cost_subtype_id.name,'account_id':record.product_id.property_account_expense and record.product_id.property_account_expense.id or (record.product_id.categ_id.property_account_expense_categ and record.product_id.categ_id.property_account_expense_categ.id),'quantity':1,'uos_id':record.product_id.uom_id.id,'price_unit':amount}
		#raise osv.except_osv(_('Information !'), _('Record has been added to Supplier Invoice.'))
		self.pool['account.invoice.line'].create(cr, uid, rent_vals,context=context)		
		record.invoice_id=True 
		