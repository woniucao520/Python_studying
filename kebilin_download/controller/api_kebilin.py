# -*- coding:utf-8 -*-
from odoo import http, SUPERUSER_ID
from odoo.http import request
import json


class KebilinAPI(http.Controller):

    @http.route('/download_kebilin/<string:sku>', type='http', auth="public")
    def download_kebilin(self, sku=None):
        try:
            kebilin = http.request.env['api.kebilin']
            folder_path = kebilin.create_main_folder()
            res = kebilin.getProductInfo(sku)
            res = json.loads(res)
            kebilin.create_excel_file(res, folder_path)
            kebilin.download_image(res, folder_path)
            #print folder_path
            filename = kebilin.file_pack(folder_path)
        except Exception, e:
            return {'Error': e}
        # file = '/var/folders/89/xnbhp5f13slf50ztzd6d10800000gn/T/tmpImO_cV/kb.zip'

        headers = [('Content-Type', u'application/zip'),
                   ('X-Content-Type-Options', 'nosniff'),
                   ('ETag', '"52ffde21e8494bec19b7e12099579942"'),
                   ('Cache-Control', 'max-age=0'),
                   ('Content-Disposition', u'attachment; filename=' + filename)]

        with open(filename, 'rb') as f:
            content_base64 = f.read()
        headers.append(('Content-Length', len(content_base64)))
        response = request.make_response(content_base64, headers)

        return response

