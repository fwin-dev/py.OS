import OS, OS.pkg

import unittest

class Test_Pkg(unittest.TestCase):
	def tearDown(self):
		OS.pkg.install("nano")
	def test_isAvailable(self):
		self.assertTrue(OS.pkg.isAvailable("nano"))
	def test_isInstalled(self):
		self.test_install("nano")
		self.assertTrue(OS.pkg.isInstalled("nano"))
	def test_install(self):
		self.assertIsNone(OS.pkg.install("nano"))
	def test_remove(self):
		self.assertIsNone(OS.pkg.remove("nano"))

if __name__ == "__main__":
	unittest.main()
