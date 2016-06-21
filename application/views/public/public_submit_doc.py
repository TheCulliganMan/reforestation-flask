# -*- coding: utf-8 -*-

import io
import csv
import xlrd

from flask.views import View


from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import flash, redirect, url_for, render_template, request
from werkzeug import parse_options_header

from decorators import admin_required

from models import DocModel
from models import PasskeyModel

def search_for_gps_sheet(wb):
        """Returns Sheet Named GPS"""
        sheetname = wb.sheet_names()
        for num, item in enumerate(sheetname):
                if item == u"GPS":
                        return num
        return False


def sheet_generator(sheet):
        """GENERATES ROWS OF A SHEET"""
        for index in range(sheet.nrows):
                yield sheet.row_values(index)


def parse_sheet(sheet, csv_out_handle=None):
        """READS SHEET AND OUTPUTS NEW CSV"""
        ID_SET = set()
        sheet_gen = sheet_generator(sheet)
        headers = (0, 1)
        count = 0
        for num, row in enumerate(sheet_gen):
                if num in headers:
                        continue
                else:
                        if row[0] in ID_SET:
                                dup = "True"
                        else:
                                dup = "False"
                        ID_SET.add(row[0])
                        try:
                                if csv_out_handle:
                                        csv_out_handle.write(
                                            "{},{},{},{},{}\n".format(row[0],
                                                                      row[1],
                                                                      row[9],
                                                                      row[13],
                                                                      dup)
                                        )
                                count += 1
                        except IndexError:
                                continue
        return count

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


def parse_csv(f):
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    try:
        wb = xlrd.open_workbook(file_path)
        print_flush("{}% PARSING {}".format(progress,
                                            file_path))
    except:
        flash(u"Passkey was incorrect", 'danger')
        return redirect(url_for('list_docs'))

    gps = wb.sheet_by_index(0)
    count = parse_sheet(gps)
    return wb


class PublicSubmitDoc(View):
    
    @admin_required
    def dispatch_request(self):

        if request.method == 'POST': 
            from_profile = False

            if "passkey" in request.form:
                passkey =  request.form["passkey"]
                passkeys = PasskeyModel.query(PasskeyModel.passkey==passkey)
                passkeys = list(passkeys)
                if not len(passkeys):
                    flash(u"Passkey was incorrect", 'danger')
                    return redirect(url_for('list_docs'))

            else:
                flash(u"Passkey was missing")
                return redirect(url_for('list_docs'))
            
            if "file" in request.files:
                f = request.files['file']
            else:
                flash(u"DocModel load Failed, No file", 'danger')
                return redirect(url_for('list_docs'))

            if "caption" in request.form:
                caption =  request.form["caption"]



            headers = f.headers
            filename = str(headers['Content-Disposition'].rsplit('filename="', 1)[-1][:-1])
            header = headers['Content-Type']
        
            parsed_header = parse_options_header(header)

            blob_key = parsed_header[1]['blob-key']

            document = DocModel(
                    user = users.get_current_user().user_id(),
                    filename = filename,
                    caption = caption,
                    blob_key = blob_key,
                )

            try:
                document.put()
                doc_id = document.key.id()
                flash(u'doc %s successfully saved.' % doc_id, 'success')
                if from_profile:
                    return redirect(url_for('list_docs'))
                
            except CapabilityDisabledError:
                flash(u'App Engine Datastore is currently in read-only mode.', 'info')
                if from_profile:
                    return redirect(url_for('list_docs'))

            return redirect(url_for('list_docs'))
            

        
