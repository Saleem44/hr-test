/** @odoo-module **/

import { UserMenu } from "@web/webclient/user_menu/user_menu";
// import { userMenuRegistry } from "@web/webclient/user_menu/user_menu";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";


const userMenuRegistry = registry.category("user_menuitems");

patch(UserMenu.prototype, {

    getElements() {
        const excludeItems = ["Support", "My Odoo.com account", "Documentation"];
        const sortedItems = userMenuRegistry
            .getAll()
            .map((element) => element(this.env))
            .filter(item => !excludeItems.includes(item.description))
            .sort((x, y) => {
                const xSeq = x.sequence ? x.sequence : 100;
                const ySeq = y.sequence ? y.sequence : 100;
                return xSeq - ySeq;
            });
        return sortedItems;
    }


});

