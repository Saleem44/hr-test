/** @odoo-module **/

import { registry } from "@web/core/registry";
// import { shortCutsItem } from "@web/webclient/user_menu/user_menu_items";
// import { logOutItem } from "@web/webclient/user_menu/user_menu_items";
import { hrPreferencesItem } from "@hr/user_menu/my_profile";

export function CustomPreferencesItem(env)  {
    return Object.assign(
        {}, 
        hrPreferencesItem(env),
        {
            sequence:  1,
        }
    );
}

// function CustomShortCutsItem(env)  {
//     return Object.assign(
//         {}, 
//         shortCutsItem(env),
//         {
//             sequence:  2,
//         }
//     );
// }

// export function CustomLogOutItem(env)  {
//     return Object.assign(
//         {}, 
//         logOutItem(env),
//         {
//             sequence:  3,
//         }
//     );
// }


registry
    .category("user_menuitems")
    .add('profile', CustomPreferencesItem, { force: true })
    // .add('shortcuts', CustomShortCutsItem, { force: true })
    // .add('log_out', CustomLogOutItem, { force: true })
