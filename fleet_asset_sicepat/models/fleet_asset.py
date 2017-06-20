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

	# def confirm_vehicle(self, cr, uid, ids, context=None):
	#	 if context is None:
	#		 context = {}
	#	 return self.write(cr, uid, ids, {
	#		 'state':'open'
	#	 }, context)