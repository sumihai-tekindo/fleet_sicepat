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
