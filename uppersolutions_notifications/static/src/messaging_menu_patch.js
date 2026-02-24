/** @odoo-module **/

import { MessagingMenu } from "@mail/core/public_web/messaging_menu";
import { patch } from "@web/core/utils/patch";

patch(MessagingMenu.prototype, {
    get canPromptToInstall() {
        return false;
    },
    get shouldAskPushPermission() {
        return false;
    },
    get threads() {
        const _threads = super.threads;
        if (this.store.discuss.activeTab === "notification") {
            // Only show threads if they have unread messages or pending actions
            return _threads.filter(t => t.isUnread || t.needactionCounter > 0);
        }
        return _threads;
    }
});
