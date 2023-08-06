"""Schwab checking account (bank) ofx importer for beancount."""

from beancount_reds_importers.libimport import banking, ofxreader


class Importer(banking.Importer, ofxreader.Importer):
    def custom_init(self):
        if not self.custom_init_run:
            self.max_rounding_error = 0.04
            self.account_number_field = 'account_id'
            self.filename_identifier_substring = 'transactions'
            self.filename_identifier_substring = 'schwabbank.ofx'
            self.custom_init_run = True
