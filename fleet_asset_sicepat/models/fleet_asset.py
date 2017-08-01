import time
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp.tools import float_is_zero
import openerp.addons.decimal_precision as dp
from openerp.tools import float_compare
from openerp.tools.translate import _

class account_asset_category(osv.osv):
	_inherit = 'account.asset.category'

	_columns = {
		'vehicle': fields.boolean('Vehicle'),
	}


class account_asset_asset(osv.osv):
	_inherit = 'account.asset.asset'

	_columns={
		'vehicle': fields.boolean('Vehicle'),
		'nomor_polisi': fields.char('No. Polisi', required=False),
		'model_name': fields.many2one('fleet.vehicle.model',"Model Name", required=False),
		# 'model_brand': fields.related('model_name','brand_id',string="Model Brand", readonly=True, type="many2one", relation="fleet.vehicle.model.brand"),
		'nomor_mesin': fields.char("No. Mesin", required=False),
		'warna': fields.char("Warna", required=False),
		'tahun_pembuatan': fields.char("Tahun Pembuatan", required=False),
		'confirmed': fields.boolean("Confirmed"),
		'vin_sn': fields.char("No. Rangka", required=False),
		'stnk': fields.char("No. STNK", required=False),
		'bpkb': fields.char("No. BPKB", required=False),
		'kir': fields.char("No. Buku KIR", required=False),
		'fuel_type': fields.selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], 'Fuel Type', help='Fuel Used by the vehicle',required=False),
		'tipe_kendaraan':fields.selection([('roda2', 'Roda 2'),('roda3','Roda 3'),('roda4','Roda 4'),('rodalebih','Roda >4')], 'Tipe Kendaraan', required=False),
		'transmission': fields.selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission', help='Transmission Used by the vehicle',required=False),
		'fleet_id':fields.many2one('fleet.vehicle',"Fleet",required=False)
	}



	_defaults = {
		'vehicle':False
	}

	def onchange_category_id(self,cr,uid,ids,category_id,context=None):
		value = {'vehicle':False}
		if category_id:
			category = self.pool.get("account.asset.category").browse(cr,uid,category_id)
			if category.vehicle:
				print "=================",category.vehicle
				value.update({'vehicle':True})
		return {'value':value}


	def confirm_vehicle(self, cr, uid, ids, context=None):
		if context is None:
			context = {}

		for asset in self.browse(cr,uid,ids):
			if asset.category_id and asset.category_id.vehicle==True:
				vals = {
                    'model_id': asset.model_name.id,
                    'license_plate':asset.nomor_polisi,
                    'vin_sn':asset.vin_sn,
                    'stnk':asset.stnk,
                    'bpkb':asset.bpkb,
                    'kir':asset.kir,
                    'stnk':asset.stnk,
                    'no_mesin':asset.nomor_mesin,
                    'tahun_pembuatan':asset.tahun_pembuatan,
                    'analytic_account':asset.account_analytic_id.id,
                    'color':asset.warna,
                    'tipe_kendaraan':asset.tipe_kendaraan,
                    'fuel_type':asset.fuel_type,
                    'transmission':asset.transmission,
                }

               	fleet_id = self.pool.get('fleet.vehicle').create(cr, uid, vals, context=context)

		return self.write(cr, uid, ids, {
			'state':'open',
			'confirmed':True,
		}, context)

