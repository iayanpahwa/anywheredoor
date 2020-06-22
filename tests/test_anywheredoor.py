# -----------------------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2020 Ayan Pahwa 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# Author : Ayan Pahwa <codensolder@gmail.com>
# -----------------------------------------------------------------------------------------


import sys
sys.path.append("..")
import unittest
from cryptography.fernet import Fernet
from anywheredoor import anywheredoor as ad

class TestAnywheredoor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global key
        key = ad.generateNewKey()

    @classmethod 
    def tearDownClass(cls):
        pass


    def test_checkEncryptionKey(self):
        self.assertTrue(ad.checkEncryptionKey(key))
        self.assertTrue(ad.checkEncryptionKey("9X8isA8ISuVL3y4MVZ5ztGjw7mLhWiezgIpo4cJpqzA="))
        self.assertTrue(ad.checkEncryptionKey("EGWU0kYny8Ma55c1j6ni2mDxhEygMKLeW8REBRd4ui4="))
        self.assertFalse(ad.checkEncryptionKey("EGWU0kYny8Ma55c1j6ni2mDxhEygMKLeW8REBRd4ui4"))
        self.assertFalse(ad.checkEncryptionKey("raNdOm K3Y"))
        self.assertFalse(ad.checkEncryptionKey("alpHA-9um3riC8937"))

        
if __name__ == '__main__':
    unittest.main()