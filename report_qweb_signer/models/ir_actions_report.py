# Copyright 2015 Tecnativa - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
from contextlib import closing
import os
import subprocess
import tempfile
import time

from odoo import models, api, _
from odoo.exceptions import UserError, AccessError
from odoo.tools.safe_eval import safe_eval

from pyhanko import stamp
from pyhanko.pdf_utils import text, images, layout
from pyhanko.sign import fields, signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
import fitz
import uuid

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


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _certificate_get(self, res_ids):
        """Obtain the proper certificate for the report and the conditions."""
        if self.report_type != 'qweb-pdf':
            return False
        certificates = self.env['report.certificate'].search([
            ('company_id', '=', self.env.user.company_id.id),
            ('model_id', '=', self.model),
        ])
        if not certificates:
            return False
        for cert in certificates:
            # Check allow only one document
            if cert.allow_only_one and len(self) > 1:
                _logger.debug(
                    "Certificate '%s' allows only one document, "
                    "but printing %d documents",
                    cert.name, len(res_ids))
                continue
            # Check domain
            if cert.domain:
                domain = [('id', 'in', tuple(res_ids))]
                domain = domain + safe_eval(cert.domain)
                docs = self.env[cert.model_id.model].search(domain)
                if not docs:
                    _logger.debug(
                        "Certificate '%s' domain not satisfied", cert.name)
                    continue
            # Certificate match!
            return cert
        return False

    def _attach_filename_get(self, res_ids, certificate):
        if len(res_ids) != 1:
            return False
        doc = self.env[certificate.model_id.model].browse(res_ids[0])
        return safe_eval(certificate.attachment, {
            'object': doc,
            'time': time
        })

    def _attach_signed_read(self, res_ids, certificate):
        if len(res_ids) != 1:
            return False
        filename = self._attach_filename_get(res_ids, certificate)
        if not filename:
            return False
        attachment = self.env['ir.attachment'].search([
            ('datas_fname', '=', filename),
            ('res_model', '=', certificate.model_id.model),
            ('res_id', '=', res_ids[0]),
        ], limit=1)
        if attachment:
            return base64.decodestring(attachment.datas)
        return False

    def _attach_signed_write(self, res_ids, certificate, signed):
        if len(res_ids) != 1:
            return False
        filename = self._attach_filename_get(res_ids, certificate)
        if not filename:
            return False
        try:
            attachment = self.env['ir.attachment'].create({
                'name': filename,
                'datas': base64.encodestring(signed),
                'datas_fname': filename,
                'res_model': certificate.model_id.model,
                'res_id': res_ids[0],
            })
        except AccessError:
            raise UserError(
                _('Saving signed report (PDF): '
                  'You do not have enough access rights to save attachments'))
        return attachment

    def _signer_bin(self, opts):
        me = os.path.dirname(__file__)
        irc_param = self.env['ir.config_parameter'].sudo()
        java_bin = 'java -jar'
        java_param = irc_param.get_param('report_qweb_signer.java_parameters')
        jar = '{}/../static/jar/jPdfSign.jar'.format(me)
        return '%s %s %s %s' % (java_bin, java_param, jar, opts)

    def pdf_sign(self, pdf, certificate):
        pdfsigned = pdf + '.signed.pdf'
        p12 = _normalize_filepath(certificate.path)
        passwd = _normalize_filepath(certificate.password_file)
        with open(passwd, 'rb') as f:
            passphrase = f.read()
        if not (p12 and passwd):
            raise UserError(
                _('Signing report (PDF): '
                  'Certificate or password file not found'))

        # Fetch coordinates based on keyword
        doc = fitz.open(pdf)
        x1,y1,x2,y2 = 350,20,550,80
        for page in doc:
            search_rects = []
            on_page = 0
            if certificate.keyword:
                search_rects = page.search_for(certificate.keyword)

            if len(search_rects) > 0:
                on_page = -1
                rect = search_rects[0]
                if rect:
                    x1,y1 = rect.x0, page.rect.y1 - rect.y1 - certificate.signature_height - rect.height
            if certificate.signature_width > 1:
                x2 = x1 + certificate.signature_width
            if certificate.signature_height > 1:
                y2 = y1 + certificate.signature_height

        me = os.path.dirname(__file__)
        background = '{}/../static/src/image/stamp.png'.format(me)

        if certificate.stamp:
            image = base64.b64decode(certificate.stamp)
            fd, background = tempfile.mkstemp()
            with closing(os.fdopen(fd, 'wb')) as f:
                f.write(image)

        # Start signing
        signer = signers.SimpleSigner.load_pkcs12(pfx_file=p12, passphrase=passphrase)
        sig_name = str(uuid.uuid1())
        with open(pdf, 'rb') as inf:
            w = IncrementalPdfFileWriter(inf, strict=False)
            fields.append_signature_field(
                w, sig_field_spec = fields.SigFieldSpec(sig_name, on_page = on_page, box=(x1,y1,x2,y2))
            )
            meta = signers.PdfSignatureMetadata(field_name='Signature')
            if certificate.show_signer:
                stamp_text = 'Digitally signed by: %(signer)s\nDate: %(ts)s'
            else:
                stamp_text = ''
            pdf_signer = signers.PdfSigner(
                meta, signer=signer, stamp_style = stamp.TextStampStyle(
                    stamp_text = stamp_text,
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

        if certificate.stamp:
            try:
                os.unlink(background)
            except (OSError, IOError):
                _logger.error('Error when trying to remove file %s', fname)
        #signer_opts = '"%s" "%s" "%s" "%s"' % (p12, pdf, pdfsigned, passwd)
        #signer = self._signer_bin(signer_opts)
        #process = subprocess.Popen(
        #    signer, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #out, err = process.communicate()
        #if process.returncode:
        #    raise UserError(
        #        _('Signing report (PDF): jPdfSign failed (error code: %s). '
        #          'Message: %s. Output: %s') %
        #        (process.returncode, err, out))
        return pdfsigned

    @api.multi
    def render_qweb_pdf(self, res_ids=None, data=None):
        certificate = self._certificate_get(res_ids)
        if certificate and certificate.attachment:
            signed_content = self._attach_signed_read(res_ids, certificate)
            if signed_content:
                _logger.debug(
                    "The signed PDF document '%s/%s' was loaded from the "
                    "database", self.report_name, res_ids,
                )
                return signed_content, 'pdf'
        content, ext = super(IrActionsReport, self).render_qweb_pdf(res_ids,
                                                                    data)
        if certificate:
            # Creating temporary origin PDF
            pdf_fd, pdf = tempfile.mkstemp(
                suffix='.pdf', prefix='report.tmp.')
            with closing(os.fdopen(pdf_fd, 'wb')) as pf:
                pf.write(content)
            _logger.debug(
                "Signing PDF document '%s' for IDs %s with certificate '%s'",
                self.report_name, res_ids, certificate.name,
            )
            signed = self.pdf_sign(pdf, certificate)
            # Read signed PDF
            if os.path.exists(signed):
                with open(signed, 'rb') as pf:
                    content = pf.read()
            # Manual cleanup of the temporary files
            for fname in (pdf, signed):
                try:
                    os.unlink(fname)
                except (OSError, IOError):
                    _logger.error('Error when trying to remove file %s', fname)
            if certificate.attachment:
                self._attach_signed_write(res_ids, certificate, content)
        return content, ext
