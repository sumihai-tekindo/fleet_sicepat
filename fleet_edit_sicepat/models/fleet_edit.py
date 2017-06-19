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
	}

	def document_complete(self,cr,uid,ids,context=None):
		return self.write(cr, uid, ids, {'state': 'completed'}, context=context)






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