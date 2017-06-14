from openerp import fields,models
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap

class FleetTools(models.Model):
    _name='fleet.tools'
    
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string="Deskripsi")
    required = fields.Boolean(string="Required")



class VehicleFleetTools(models.Model):
    _name='vehicle.fleet.tools'

    fleet_id=fields.Many2one('fleet.vehicle',"Vehicle")
    tool_id=fields.Many2one('fleet.tools',"Tools")
    availability=fields.Boolean('Availability')
    notes=fields.Text("Notes")