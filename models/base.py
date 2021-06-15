# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).
from odoo import api, models


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def search_links(self, relation_name):
        return self.env["sync.link"]._search_links_external(
            relation_name, dict(), model=self._name, make_logs=True
        )

    def set_link(self, relation_name, ref, sync_date=None, allow_many2many=False):
        return self.env["sync.link"]._set_link_odoo(
            self, relation_name, ref, sync_date, allow_many2many
        )

    def search_links(self, relation_name, refs=None):
        return self.env["sync.link"]._search_links_odoo(self, relation_name, refs)
