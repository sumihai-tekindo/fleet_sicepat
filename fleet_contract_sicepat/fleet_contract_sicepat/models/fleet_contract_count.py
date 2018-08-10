
from openerp import models, fields, api, _


	
class fleet_vehicle_contract(models.Model):
	_inherit = 'fleet.vehicle.log.contract'


	@api.multi
	def _count_supplier_invoice(self):
		
		insurer_id_obj = self.env['account.invoice']
		self.count_supplier_invoice=insurer_id_obj.search_count([('partner_id', '=', self.insurer_id.id)])


	@api.multi	
	def return_supplier_invoice(self):
		domain = ([('partner_id', '=', self.insurer_id.id)])
	
		return {
			'type': 'ir.actions.act_window',
			'name': _('Supplier Invoice'),
			'res_model': 'account.invoice_tree',
			'view_type': 'tree',
			'view_mode': 'tree',
			#'res_id': self.insurer_id.id,
			'target': 'current',	
			'domain': domain,
			'nodestroy': True,
			#'flags': {'form': {'action_buttons': True}}

				}

	count_supplier_invoice = fields.Integer(compute=_count_supplier_invoice,default=0)