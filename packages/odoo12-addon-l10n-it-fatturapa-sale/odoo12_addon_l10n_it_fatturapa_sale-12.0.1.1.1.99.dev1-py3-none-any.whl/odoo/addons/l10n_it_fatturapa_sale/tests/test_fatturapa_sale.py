#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestFatturapaSale(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner_id = self.env['res.partner'] \
            .name_create("Test partner")[0]
        self.product_id = self.env['product.product'] \
            .name_create("Test product")[0]

    def _create_order(self):
        sale_order = self.env['sale.order'].create([{
            'partner_id': self.partner_id,
            'related_documents': [(0, 0, {
                'type': 'order',
                'name': 'order1',
            })],
        }])
        order_line = self.env['sale.order.line'].create([{
            'order_id': sale_order.id,
            'product_id': self.product_id,
            'product_uom_qty': 1,
            'admin_ref': 'line admin ref',
            'related_documents': [(0, 0, {
                'type': 'order',
                'name': 'line1',
            })],
        }])
        sale_order.action_confirm()
        return order_line, sale_order

    def test_create_invoice(self):
        """
        Generate an invoice from a sale order.
        Check that related documents are passed
        from the sale order (and its lines) to the invoice (and its lines).
        """
        order_line, sale_order = self._create_order()

        # Check the invoice
        invoice_ids = sale_order.action_invoice_create()
        self.assertEqual(len(invoice_ids), 1,
                         "Multiple invoices for sale order")
        invoice = self.env['account.invoice'].browse(invoice_ids)
        self.assertEqual(
            invoice.related_documents,
            sale_order.related_documents)

        # Check the invoice line
        invoice_line = invoice.invoice_line_ids.filtered(
            lambda l: order_line in l.sale_line_ids)
        self.assertEqual(len(invoice_line), 1,
                         "Multiple invoice lines for sale order line")

        self.assertEqual(
            invoice_line.related_documents,
            order_line.related_documents)
        self.assertEqual(
            invoice_line.admin_ref,
            order_line.admin_ref)

    def test_create_invoice_multiple(self):
        """
        Generate a grouping invoice from multiple orders.
        Check that related documents are passed
        from the sale orders (and their lines)
        to the invoice (and its lines).
        """
        order_line1, sale_order1 = self._create_order()
        order_line2, sale_order2 = self._create_order()
        sale_orders = sale_order1 | sale_order2
        sale_orders_lines = order_line1 | order_line2

        # Check the invoice
        invoice_ids = sale_orders.action_invoice_create()
        self.assertEqual(len(invoice_ids), 1,
                         "Multiple invoices for sale order")
        invoice = self.env['account.invoice'].browse(invoice_ids)
        self.assertEqual(
            invoice.related_documents,
            sale_orders.mapped('related_documents'))

        # Check the invoice lines
        self.assertEqual(
            invoice.invoice_line_ids.mapped('related_documents'),
            sale_orders_lines.mapped('related_documents'))

    def test_keep_document(self):
        """
        Delete an invoice having related documents.
        Check that the related documents are no more deleted
        if linked to a sale order.
        """
        order_line, sale_order = self._create_order()

        invoice_ids = sale_order.action_invoice_create()
        self.assertEqual(len(invoice_ids), 1,
                         "Multiple invoices for sale order")
        invoice = self.env['account.invoice'].browse(invoice_ids)
        related_documents = invoice.related_documents

        # Delete the invoice: the related document persists
        invoice.unlink()
        self.assertTrue(related_documents.exists())

        # Delete the sale order: the related document is deleted too
        sale_order.action_cancel()
        sale_order.unlink()
        self.assertFalse(related_documents.exists())
