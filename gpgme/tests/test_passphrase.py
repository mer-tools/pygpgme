import unittest
import os
import StringIO
from textwrap import dedent

import gpgme
from gpgme.tests.util import GpgHomeTestCase

class PassphraseTestCase(GpgHomeTestCase):

    import_keys = ['passphrase.pub', 'passphrase.sec']

    def test_sign_without_passphrase_cb(self):
        ctx = gpgme.Context()
        key = ctx.get_key('EFB052B4230BBBC51914BCBB54DCBBC8DBFB9EB3')
        ctx.signers = [key]
        plaintext = StringIO.StringIO('Hello World\n')
        signature = StringIO.StringIO()

        try:
            new_sigs = ctx.sign(plaintext, signature, gpgme.SIG_MODE_CLEAR)
        except gpgme.error, e:
            self.assertEqual(e[1], 'Bad passphrase')
        else:
            self.fail('gpgme.error not raised')

    def passphrase_cb(self, uid_hint, passphrase_info, prev_was_bad, fd):
        self.uid_hint = uid_hint
        self.passphrase_info = passphrase_info
        self.prev_was_bad = prev_was_bad
        os.write(fd, 'test\n')

    def test_sign_with_passphrase_cb(self):
        ctx = gpgme.Context()
        key = ctx.get_key('EFB052B4230BBBC51914BCBB54DCBBC8DBFB9EB3')
        ctx.signers = [key]
        ctx.passphrase_cb = self.passphrase_cb
        plaintext = StringIO.StringIO('Hello World\n')
        signature = StringIO.StringIO()

        self.uid_hint = None
        self.passphrase_info = None
        self.prev_was_bad = None
        new_sigs = ctx.sign(plaintext, signature, gpgme.SIG_MODE_CLEAR)

        # ensure that passphrase_cb has been run, and the data it was passed
        self.assertEqual(self.uid_hint,
            '54DCBBC8DBFB9EB3 Passphrase (test) <passphrase@example.org>')
        self.assertEqual(self.passphrase_info,
            '54DCBBC8DBFB9EB3 54DCBBC8DBFB9EB3 17 0')
        self.assertEqual(self.prev_was_bad, False)

        self.assertEqual(new_sigs[0].type, gpgme.SIG_MODE_CLEAR)
        self.assertEqual(new_sigs[0].fpr,
                        'EFB052B4230BBBC51914BCBB54DCBBC8DBFB9EB3')

def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromName(__name__)
