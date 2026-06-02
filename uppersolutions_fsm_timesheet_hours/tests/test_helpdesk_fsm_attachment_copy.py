import base64

from odoo.addons.helpdesk.tests.common import HelpdeskCommon
from odoo.tests import Form, tagged


@tagged("-at_install", "post_install")
class TestHelpdeskFsmAttachmentCopy(HelpdeskCommon):
    def test_ticket_attachments_are_copied_to_generated_fsm_task(self):
        self.test_team.use_fsm = True
        ticket = self.env["helpdesk.ticket"].create({
            "name": "Ticket con adjuntos",
            "partner_id": self.partner.id,
            "team_id": self.test_team.id,
        })

        self.env["ir.attachment"].create([
            {
                "name": "parte.pdf",
                "datas": base64.b64encode(b"contenido-parte"),
                "res_model": ticket._name,
                "res_id": ticket.id,
            },
            {
                "name": "foto.jpg",
                "datas": base64.b64encode(b"contenido-foto"),
                "res_model": ticket._name,
                "res_id": ticket.id,
            },
        ])

        wizard_action = ticket.action_generate_fsm_task()
        wizard = Form(
            self.env[wizard_action["res_model"]].with_context(wizard_action["context"])
        ).save()
        task = wizard.action_generate_task()

        task_attachments = self.env["ir.attachment"].search([
            ("res_model", "=", task._name),
            ("res_id", "=", task.id),
        ])

        self.assertEqual(len(task_attachments), 2)
        self.assertEqual(set(task_attachments.mapped("name")), {"parte.pdf", "foto.jpg"})
        self.assertEqual(task.helpdesk_ticket_id, ticket)

