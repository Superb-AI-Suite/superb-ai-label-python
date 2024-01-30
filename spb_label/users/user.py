from spb_label.core import Model
from spb_label.core.models.types import (
    String,

)


class User(Model):
    email = String(property_name='email')
    name = String(property_name='name')
    status = String(property_name='status')
    team_role = String(property_name='tenantRole')
    project_role = String(property_name='projectRole')
