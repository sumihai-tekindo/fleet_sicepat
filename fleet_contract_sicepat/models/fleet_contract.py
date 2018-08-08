from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
global invoice,account_id,invoice_id,insurer_id,insurer_id_obj


class account_invoice(osv.osv):
	_inherit = "account.invoice"

	_columns = {
		'fleet_log_contract_id': fields.many2one("fleet.vehicle.log.contract","Fleet Contract")
	}

class fleet_vehicle_log_contract(osv.osv):
	_inherit = 'fleet.vehicle.log.contract'


	def _count_supplier_invoice(self, cr, uid, ids, field_name, arg, context=None):
		result = {}
		contracts = self.browse(cr,uid,ids,context=context)
		invoice_ids = self.pool.get('account.invoice').search(cr,uid,[('fleet_log_contract_id','in',ids)])
		#print "xxxxxxxxxxxxxxxx",ids
		invoices = self.pool.get('account.invoice').browse(cr,uid,invoice_ids)
		#print "-----------------",invoices
		inv = {}
		for i in invoices:
			curr = 1
			if i.fleet_log_contract_id.id in inv:
				curr = inv.get(i.fleet_log_contract_id.id,0.0)
				curr+=1
			inv.update({i.fleet_log_contract_id.id:curr})
		for c in contracts:
			result.update({c.id: inv.get(c.id,0.0)})
		return result

	_columns = {
		'product_id' :fields.many2one('product.product', 'Product', required=True),
		'department_id' :fields.many2one('account.invoice.department', 'Department',required=True),
		'invoice_id':fields.boolean(default=False, copy=False),
		'count_invoice' : fields.function(_count_supplier_invoice,type="integer",string="Invoice")
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
		#Fill to the form
		vals={
			'type':'in_invoice',
			'partner_id':record.insurer_id.id,
			'account_id':record.insurer_id.property_account_payable.id,
			'currency_id':record.insurer_id.company_id.currency_id.id,
			'department_id':record.department_id,
			'date_invoice':record.date,
			'sewa':True,
			'date_start':start_date,
			'date_end':end_date1,
			'fleet_log_contract_id': record.id,
			}
		# print "vals================",vals
		account=self.pool['account.invoice'].create(cr, uid, vals,context=context) 
		product=record.product_id
		cost_subtype_id=record.cost_subtype_id.id
		amount=record.amount
		#Fill to the line
		rent_vals={'product_id':product.id, 'invoice_id':account, 'name':record.cost_subtype_id.name,'account_id':record.product_id.property_account_expense and record.product_id.property_account_expense.id or (record.product_id.categ_id.property_account_expense_categ and record.product_id.categ_id.property_account_expense_categ.id),'quantity':1,'uos_id':record.product_id.uom_id.id,'price_unit':amount}
	
		self.pool['account.invoice.line'].create(cr, uid, rent_vals,context=context)		
		record.invoice_id=True 


	
	def return_supplier_invoice(self, cr, uid, ids, insurer_id,context=None):
		contracts = self.pool.get('fleet.vehicle.log.contract').browse(cr,uid,ids,context=context)
		# partners = [c.insurer_id.id for c in contracts if c.insurer_id]
		domain = [('fleet_log_contract_id','in',ids)]
		invoice_ids = self.pool.get('account.invoice').search(cr,uid,domain)
		context_domain = [('id','in',invoice_ids)]
		return {
			'type': 'ir.actions.act_window',
			'name': 'Supplier Invoice',
			'res_model': 'account.invoice',
			'view_type': 'form',
			'view_mode': 'tree',
			#'res_id': self.insurer_id.id,
			'target': 'current',
			'domain': domain,
			'nodestroy': True,
			'flags': {'form': {'action_buttons': True}}

				}