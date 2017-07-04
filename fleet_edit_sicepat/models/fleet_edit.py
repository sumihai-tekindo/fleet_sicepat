from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta


class fleet_vehicle(osv.osv):
	_inherit = 'fleet.vehicle'

	_columns = {
		'stnk': fields.char('No. STNK', required=True),
		'bpkb': fields.char('No. BPKB', required=True),
		'kir': fields.char('No. Buku KIR', required=True),
		'no_mesin':fields.char('No. Mesin', required=True),
		'vin_sn': fields.char('No. Rangka', required=True,copy=False),
		'tahun_pembuatan':fields.char('Tahun Pembuatan', required=True),
		'analytic_account':fields.many2one('account.analytic.account', "Analytic Account", required=True),
		'tipe_kendaraan':fields.selection([('roda2', 'Roda 2'),('roda3','Roda 3'),('roda4','Roda 4'),('rodalebih','Roda >4')], 'Tipe Kendaraan', required=True),
		'sticker':fields.boolean('Sticker', required=True),
		'color': fields.char('Color', help='Color of the vehicle',required=True),
		'transmission': fields.selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission', help='Transmission Used by the vehicle',required=True),
		'fuel_type': fields.selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], 'Fuel Type', help='Fuel Used by the vehicle',required=True),
		'tools_ids': fields.one2many('vehicle.fleet.tools','fleet_id',"Tools"),
	}


class fleet_vehicle_log_contract(osv.osv):
	_inherit = 'fleet.vehicle.log.contract'

	def _computedate(self,cr,uid,ids,name,args,context=None):
		res = {}
		for fleet in self.browse(cr,uid,ids):
			res[fleet['id']]=(datetime.date.today()+relativedelta(months=1)).strftime('%Y-%m-%d')
		return res

	_columns = {
		'state': fields.selection([('open', 'In Progress'), ('completed','Document Completed'), ('toclose','To Close'), ('closed', 'Terminated')],
									'Status', readonly=True, help='Choose wheter the contract is still valid or not',
									copy=False),
		'date_computation': fields.function(_computedate,string='Computation',type="date"),
		'analytic_account': fields.many2one('account.analytic.account','Analytic Account',help="Nama Admin Cabang"),
	}

	def document_complete(self,cr,uid,ids,context=None):
		return self.write(cr, uid, ids, {'state': 'completed'}, context=context)


	def email_ganti_oli(self,cr,uid,ids,context=None):
		Mail = self.pool.get('mail.mail')
		template_id = self.pool.get('ir.model.data').get_object_reference(cr,uid,"fleet_edit_sicepat","email_template_service_ganti_oli")
		res_model, res_id = self.pool.get('ir.model.data').get_object_reference(cr, uid,'fleet','type_service_31')
		vehicle_ids = self.pool.get('fleet.vehicle').search(cr,uid,[])
		vehicle = self.pool.get('fleet.vehicle').browse(cr,uid,vehicle_ids)

		query = """select vehicle_id,value from (select 
					fvc.id,fvc.vehicle_id,fvc.odometer_id,fvo.value, 
					rank() OVER (PARTITION BY fvc.vehicle_id ORDER BY fvo.value DESC) AS rank 
					from fleet_vehicle_cost fvc
					left join fleet_vehicle_odometer fvo on fvc.odometer_id=fvo.id
					where fvc.cost_subtype_id=%s and fvc.date<now()
					order by fvo.value desc
					)dummy
					where rank=1
					"""%(res_id)
		last_services = cr.execute(query)
		result = dict(cr.fetchall())
		res = {}
		for v in vehicle:
			if (v.odometer-result.get(v.id,0.0))>=4800.0:
				res.update({
					v:{'prev':result.get(v.id,0.0),'next':v.odometer,'diff':v.odometer-result.get(v.id,0.0)}
					})

		for v in res:

			values = self.pool.get('email.template').generate_email(cr,uid,template_id[1],v.id,context=context)
			values['recipient_ids'] = [(4, pid) for pid in values.get('partner_ids', list())]
			values['email_to']=v.analytic_account and v.analytic_account.user_admin_id and v.analytic_account.user_admin_id.partner_id.email
			attachment_ids = values.pop('attachment_ids', [])
			attachments = values.pop('attachments', [])
			# add a protection against void email_from
			if 'email_from' in values and not values.get('email_from'):
				values.pop('email_from')
			mail_id = Mail.create(cr,uid,values)
			mail = Mail.browse(cr,uid,mail_id)



	def email_perpanjangan_kir(self,cr,uid,ids=None,context=None):
		Mail = self.pool.get('mail.mail')
		template_id = self.pool.get('ir.model.data').get_object_reference(cr,uid,"fleet_edit_sicepat","email_template_service_perpanjangan_kir")
		res_model, res_id = self.pool.get('ir.model.data').get_object_reference(cr, uid,'fleet_edit_sicepat','service_type_kir')
		if not ids:
			ids = self.pool.get('fleet.vehicle.log.contract').search(cr,uid,[('cost_subtype_id', '=', res_id), ('expiration_date', '<=', 'date_computation')])
		vehicle_contract = self.pool.get('fleet.vehicle.log.contract').browse(cr, uid, ids)

		for vc in vehicle_contract:
			values = self.pool.get('email.template').generate_email(cr,uid,template_id[1],vc.id,context=context)
			values['recipient_ids'] = [(4, pid) for pid in values.get('partner_ids', list())]
			values['email_to']=vc.analytic_account and vc.analytic_account.user_admin_id and vc.analytic_account.user_admin_id.partner_id.email
			attachment_ids = values.pop('attachment_ids', [])
			attachments = values.pop('attachments', [])
			# add a protection against void email_from
			if 'email_from' in values and not values.get('email_from'):
				values.pop('email_from')
			mail_id = Mail.create(cr,uid,values)
	


		


	def email_perpanjangan_stnk(self,cr,uid,ids,context=None):
		Mail = self.pool.get('mail.mail')
		template_id = self.pool.get('ir.model.data').get_object_reference(cr,uid,"fleet_edit_sicepat","email_template_perpanjangan_stnk")
		res_model, res_id = self.pool.get('ir.model.data').get_object_reference(cr, uid,'fleet_edit_sicepat','service_type_stnk')
		if not ids:
			ids = self.pool.get('fleet.vehicle.log.contract').search(cr,uid,[('cost_subtype_id', '=', res_id), ('expiration_date', '<=', 'date_computation')])
		vehicle_contract = self.pool.get('fleet.vehicle.log.contract').browse(cr, uid, ids)

		for vc in vehicle_contract:
			if (vc.cost_subtype_id==res_id & vc.expiration_date<=vc.date_computation):
				values = self.pool.get('email.template').generate_email(cr,uid,template_id[1],vc.id,context=context)
				values['recipient_ids'] = [(4, pid) for pid in values.get('partner_ids', list())]
				values['email_to']=vc.analytic_account and vc.analytic_account.user_admin_id and vc.analytic_account.user_admin_id.partner_id.email
				attachment_ids = values.pop('attachment_ids', [])
				attachments = values.pop('attachments', [])
				# add a protection against void email_from
				if 'email_from' in values and not values.get('email_from'):
					values.pop('email_from')
				mail_id = Mail.create(cr,uid,values)


	def email_perpanjangan_pajak(self,cr,uid,ids,context=None):
		Mail = self.pool.get('mail.mail')
		template_id = self.pool.get('ir.model.data').get_object_reference(cr,uid,"fleet_edit_sicepat","email_template_perpanjangan_pajak")
		res_model, res_id = self.pool.get('ir.model.data').get_object_reference(cr, uid,'fleet_edit_sicepat','service_type_pajak')
		if not ids:
			ids = self.pool.get('fleet.vehicle.log.contract').search(cr,uid,[('cost_subtype_id', '=', res_id), ('expiration_date', '<=', 'date_computation')])
		vehicle_contract = self.pool.get('fleet.vehicle.log.contract').browse(cr, uid, ids)

		for vc in vehicle_contract:
			if (vc.cost_subtype_id==res_id & vc.expiration_date<=vc.date_computation):
				values = self.pool.get('email.template').generate_email(cr,uid,template_id[1],vc.id,context=context)
				values['recipient_ids'] = [(4, pid) for pid in values.get('partner_ids', list())]
				values['email_to']=vc.analytic_account and vc.analytic_account.user_admin_id and vc.analytic_account.user_admin_id.partner_id.email
				attachment_ids = values.pop('attachment_ids', [])
				attachments = values.pop('attachments', [])
				# add a protection against void email_from
				if 'email_from' in values and not values.get('email_from'):
					values.pop('email_from')
				mail_id = Mail.create(cr,uid,values)


class fleet_vehicle_log_fuel(osv.osv):
	_inherit = 'fleet.vehicle.log.fuel'


	_columns = {
		'start_odometer': fields.float('Odometer Sekarang'),
		'last_odometer': fields.float('Odometer Terakhir'),
		'driver_id': fields.many2one('res.partner', 'Nama Supir', help='Driver of the vehicle'),
		'odometer_unit1': fields.related('vehicle_id', 'odometer_unit', type="char", string="Unit", readonly=True),
	}


class fleet_vehicle_log_services(osv.osv):
	_inherit = 'fleet.vehicle.log.services'

	_columns = {
		'analytic_account': fields.many2one('account.analytic.account','Analytic Account',help="Nama Admin Cabang")
	}