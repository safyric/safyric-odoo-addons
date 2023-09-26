import base64
import cv2
import numpy as np

from odoo import api, fields, models


class ExtractSignatureWizard(models.TransientModel):
    _name = 'extract.signature.wizard'
    _description = 'Extract Signature Wizard'

    image = fields.Binary('Image', required=True)

    @api.multi
    def extract_signature(self):
        # Load the image
        file = self.image
        encoded = file.decode('utf-8')
        nparr = np.fromstring(base64.b64decode(encoded), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Crop image
        height,width = image.shape[:2]
        x_start = int(width * 0.05)
        x_end = int(width * 0.95)
        y_start = int(height * 0.05)
        y_end = int(height * 0.95)
        image = image[y_start:y_end, x_start:x_end]

        # Cut the signature using boundingRect
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
        dilation = cv2.dilate(thresh, rect_kernel, iterations = 1)
        contours, hier = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        im2=image.copy()
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            #rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0), 2)
            cropped = im2[y:y+h, x:x+w]

        # Enhance image using morph_open
        kernel = np.ones((1,1), np.uint8)
        img = cv2.morphologyEx(cropped, cv2.MORPH_OPEN, kernel)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([0,0,0], dtype=np.uint8)
        upper = np.array([170,150,50], dtype=np.uint8)
        mask = cv2.inRange(img, lower, upper)
        image = cv2.bitwise_not(mask)

        # Transparent background
        h, w, c = img.shape
        img_bgra = np.concatenate([img, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
        white = np.all(img == [255, 255, 255], axis=-1)
        img_bgra[white, -1] = 0


        # Encode and write to field
        retval,buffer_img =cv2.imencode('.png', img_bgra)
        digital_signature = base64.b64encode(buffer_img)

        if digital_signature:
            act_close = {'type': 'ir.actions.act_window_close'}
            current = self._context.get('active_ids')
            if current is None:
                return act_close
            assert len(current) == 1, "Only 1 sale ID expected"
            rec = self.env['res.users.signatures'].browse(current)
            rec.digital_signature = digital_signature
            return act_close
