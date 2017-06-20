from openerp import fields,models,api,exceptions

class ServiceLog(models.Model):
    _inherit='fleet.vehicle.log.services'

    supir_id=fields.Many2one('res.partner', "Nik Supir", required=True)
    invoice_id=fields.Boolean(default=False)

class ServiceType_inherit(models.Model):
    _inherit='fleet.service.type'
    product_id=fields.Many2one('product.product', "Product")


class Wizard_new_invoice(models.TransientModel):
    _name = 'account.invoice.wizard'

    department_id=fields.Many2one('account.invoice.department',"department")

    @api.multi
    def subscribe(self):
        record=self.env['fleet.vehicle.log.services'].browse(self._context.get('active_id'))
        if record.invoice_id:
            raise exceptions.ValidationError("duplicate is founded! you was created this invoice,please create a new one.")
        if not record.cost_subtype_id.product_id:
            raise exceptions.ValidationError("you must choose every product of your services!")
        vals={'type':'in_invoice','partner_id':record.vendor_id.id,'account_id':record.vendor_id.property_account_payable.id,'currency_id':record.vendor_id.company_id.currency_id.id,'department_id':self.department_id.id,'date_invoice':record.date }
        account=self.env['account.invoice'].create(vals)
        product=record.cost_subtype_id.product_id
        account_coa=product.property_account_expense or product.categ_id.property_account_expense_categ
        service_vals={'invoice_id':account.id, 'product_id':product.id, 'name':record.cost_subtype_id.name,'account_id':account_coa.id,'quantity':1,'uos_id':product.uom_id.id,'price_unit':record.amount}
        self.env['account.invoice.line'].create(service_vals)
        for x in record.cost_ids:
            account_coa_loop=x.cost_subtype_id.product_id.property_account_expense or x.cost_subtype_id.product_id.categ_id.property_account_expense_categ
            service_vals_loop={'invoice_id':account.id, 'product_id':x.cost_subtype_id.product_id.id, 'name':x.cost_subtype_id.name,'account_id':account_coa_loop.id,'quantity':1,'uos_id':x.cost_subtype_id.product_id.uom_id.id,'price_unit':x.amount}
            self.env['account.invoice.line'].create(service_vals_loop)
        record.invoice_id=True
        return {'type':'ir.actions.act_window_close'}