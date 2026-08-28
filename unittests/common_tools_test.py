import unittest

from tools import common


class CommonToolsTest(unittest.TestCase):
    def test_arm64_platform_postfixes_are_available(self):
        self.assertEqual(
            "linuxarm64",
            common.OS_POSTFIX2_ARCH["LINUX"]["arm64"],
        )
        self.assertEqual(
            "linuxarm64",
            common.CEF_POSTFIX2_ARCH["LINUX"]["arm64"],
        )
        self.assertEqual(
            "manylinux_2_17_aarch64",
            common.PYPI_POSTFIX2_ARCH["LINUX"]["arm64"],
        )
        self.assertEqual(
            "macarm64",
            common.OS_POSTFIX2_ARCH["MAC"]["arm64"],
        )
        self.assertEqual(
            "macosarm64",
            common.CEF_POSTFIX2_ARCH["MAC"]["arm64"],
        )


if __name__ == "__main__":
    unittest.main()
