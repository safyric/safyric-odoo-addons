# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from pyhanko import stamp
from pyhanko.pdf_utils import text, images, layout
from pyhanko.sign import fields as field, signers
from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
import fitz

import base64
import os
import tempfile
import time
from contextlib import closing

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

import logging
_logger = logging.getLogger(__name__)

def _normalize_filepath(path):
    path = path or ''
    path = path.strip()
    if not os.path.isabs(path):
        me = os.path.dirname(__file__)
        path = '{}/../static/certificate/'.format(me) + path
    path = os.path.normpath(path)
    return path if os.path.exists(path) else False


class DmsDigitalSignature(models.TransientModel):
    _name = "dms.digital.signature"
    _description = "DMS Digital Signature"

    signature = fields.Binary(string='Signature', attachment=False)
    signature_keyword = fields.Char('Signature Area', help="Keyword to identify the signature area to attach digital signature")
    signature_width = fields.Integer('Signature Width', help="Width of the signature area")
    signature_height = fields.Integer('Signature Height', help="Height of the signature area")


    @api.multi
    def dms_digital_signature(self):
        doc_ids = self._context.get('active_ids')
        doc_id = self.env['dms.file'].browse(doc_ids)

        # Ger pkcs#12 pfx file
        certificates = self.env['report.certificate'].search([
            ('company_id', '=', self.env.user.company_id.id),
            ('model_id.model', '=', 'dms.file')
        ])
        if not certificates:
            return False

        for certificate in certificates:
            if certificate.allow_only_one and len(self) >1:
                continue
            if certificate.domain:
                domain = safe_eval(certificate.domain)
                docs = self.env[certificate.model_id.model].search(domain)
                if not docs:
                    _logger.exception(
                        "Certificate '%s' domain not satisfied", cert.name)
                    continue

        if certificate:
            p12 = _normalize_filepath(certificate.path)
            passwd = _normalize_filepath(certificate.password_file)
            with open(passwd, 'rb') as f:
                passphrase = f.read()
            if not (p12 and passwd):
               raise UserError(
                   _('Signing report (PDF): '
                     'Certificate or password file not found'))

            # Fetch coordinates based on keyword
            content = base64.b64decode(doc_id.content)
            if certificate:
                pdf_fd, pdf = tempfile.mkstemp()
                with closing(os.fdopen(pdf_fd, 'wb')) as pf:
                    pf.write(content)

            doc = fitz.open(pdf)
            x1,y1,x2,y2 = 350,20,550,80

            if self.signature_keyword:
                keyword = self.signature_keyword
            else:
                keyword = certificate.keyword

            if self.signature_width > 0 or self.signature_width >0:
                width, height = self.signature_width, self.signature_height
            else:
                width, height = certificate.signature_width, certificate.signature_height
            for page in doc:
                search_rects = []
                on_page = 0
                if keyword:
                    search_rects = page.search_for(keyword)

                if len(search_rects) > 0:
                    on_page = -1
                    rect = search_rects[0]
                    if rect:
                        x1,y1 = rect.x0, page.rect.y1 - rect.y1 - height * 1.02
                if width > 1:
                    x2 = x1 + width

                if height > 1:
                    y2 = y1 + height

            me = os.path.dirname(__file__)
            background = '{}/../static/src/image/stamp.png'.format(me)

            if self.signature:
                sig_image = self.signature
            else:
                sig_image = certificate.stamp

            if sig_image:
                image = base64.b64decode(sig_image)
                fd, background = tempfile.mkstemp()
                with closing(os.fdopen(fd, 'wb')) as f:
                   f.write(image)

            # Start signing
            pdfsigned = pdf + '-signed.pdf'
            signer = signers.SimpleSigner.load_pkcs12(pfx_file=p12, passphrase=passphrase)
            with open(pdf, 'rb') as inf:
                w = IncrementalPdfFileWriter(inf)
                field.append_signature_field(
                    w, sig_field_spec = field.SigFieldSpec('Signature', on_page = on_page, box=(x1,y1,x2,y2))
                )
                meta = signers.PdfSignatureMetadata(field_name='Signature')
                pdf_signer = signers.PdfSigner(
                    meta, signer=signer, stamp_style = stamp.TextStampStyle(
                        stamp_text = 'Digitally signed by: %(signer)s\nDate: %(ts)s',
                        background = images.PdfImage(background),
                        background_layout = layout.SimpleBoxLayoutRule(
                            x_align=layout.AxisAlignment(2),
                            y_align=layout.AxisAlignment(2),
                            margins=layout.Margins(left=5, right=5, top=5, bottom=15),
                        ),
                        inner_content_layout = layout.SimpleBoxLayoutRule(
                            x_align=layout.AxisAlignment(1),
                            y_align=layout.AxisAlignment(1),
                        ),
                        border_width = 0,
                        background_opacity = 1
                    )
                )
                with open(pdfsigned, 'wb') as outf:
                    pdf_signer.sign_pdf(w, output=outf)

                if pdfsigned:
                    with open(pdfsigned, 'rb') as f:
                        signed_doc = base64.b64encode(f.read())
                    act_close = {'type': 'ir.actions.act_window_close'}
                    current = self._context.get('active_ids')
                    if current is None:
                        return act_close
                    assert len(current) == 1, "Only 1 ID expected"
                    rec = self.env['dms.file'].browse(current)
                    rec.signed_doc = signed_doc
                    name, extension = os.path.splitext(rec.name)
                    name = name + '-signed' + extension
                    rec.signed_doc_name = name
                    return act_close


                for fname in (pdf, pdfsigned):
                    try:
                        os.unlink(fname)
                    except (OSError, IOError):
                        _logger.error('Error when trying to remove file %s', fname)

            if sig_image:
                try:
                    os.unlink(background)
                except (OSError, IOError):
                    _logger.error('Error when trying to remove file %s', fname)

