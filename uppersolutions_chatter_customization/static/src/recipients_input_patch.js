/** @odoo-module */

import { RecipientsInput } from "@mail/core/web/recipients_input";
import { Composer } from "@mail/core/common/composer";
import { patch } from "@web/core/utils/patch";
import { toRaw } from "@odoo/owl";

patch(RecipientsInput.prototype, {
    setup() {
        super.setup(...arguments);
        
        // Clear suggested and additional recipients on setup so the list starts empty
        if (this.props.thread) {
            if (this.props.thread.suggestedRecipients) {
                this.props.thread.suggestedRecipients = [];
            }
            if (this.props.thread.additionalRecipients) {
                this.props.thread.additionalRecipients = [];
            }
        }
    },

    getPlaceholder() {
        const hasRecipients =
            this.props.thread?.suggestedRecipients?.length ||
            this.props.thread?.additionalRecipients?.length;
        return hasRecipients ? "" : ""; // Removed "Followers only" translated string
    }
});

patch(Composer.prototype, {
    async _sendMessage(value, postData, extraData) {
        if (this.props.type !== "note" && this.props.composer && this.props.composer.thread) {
            const thread = toRaw(this.props.composer.thread);
            const allRecipients = [
                ...(thread.suggestedRecipients || []),
                ...(thread.additionalRecipients || []),
            ];
            
            // If the user left the recipients input completely empty
            if (allRecipients.length === 0) {
                extraData = extraData || {};
                extraData.context = extraData.context || {};
                extraData.context.chatter_empty_recipients = true;
            }
        }
        return super._sendMessage(value, postData, extraData);
    }
});
