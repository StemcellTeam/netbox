from django.test import TestCase

from utilities.forms import *


class ExpandIPAddress(TestCase):
    """
    Validate the operation of expand_ipaddress_pattern().
    """
    def test_ipv4_range(self):
        input = '1.2.3.[9-10]/32'
        output = sorted([
            '1.2.3.9/32',
            '1.2.3.10/32',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 4)), output)

    def test_ipv4_set(self):
        input = '1.2.3.[4,44]/32'
        output = sorted([
            '1.2.3.4/32',
            '1.2.3.44/32',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 4)), output)

    def test_ipv4_multiple_ranges(self):
        input = '1.[9-10].3.[9-11]/32'
        output = sorted([
            '1.9.3.9/32',
            '1.9.3.10/32',
            '1.9.3.11/32',
            '1.10.3.9/32',
            '1.10.3.10/32',
            '1.10.3.11/32',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 4)), output)

    def test_ipv4_multiple_sets(self):
        input = '1.[2,22].3.[4,44]/32'
        output = sorted([
            '1.2.3.4/32',
            '1.2.3.44/32',
            '1.22.3.4/32',
            '1.22.3.44/32',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 4)), output)

    def test_ipv4_set_and_range(self):
        input = '1.[2,22].3.[9-11]/32'
        output = sorted([
            '1.2.3.9/32',
            '1.2.3.10/32',
            '1.2.3.11/32',
            '1.22.3.9/32',
            '1.22.3.10/32',
            '1.22.3.11/32',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 4)), output)

    def test_ipv6_range(self):
        input = 'fec::abcd:[9-b]/64'
        output = sorted([
            'fec::abcd:9/64',
            'fec::abcd:a/64',
            'fec::abcd:b/64',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 6)), output)

    def test_ipv6_range_multichar_field(self):
        input = 'fec::abcd:[f-11]/64'
        output = sorted([
            'fec::abcd:f/64',
            'fec::abcd:10/64',
            'fec::abcd:11/64',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 6)), output)

    def test_ipv6_set(self):
        input = 'fec::abcd:[9,ab]/64'
        output = sorted([
            'fec::abcd:9/64',
            'fec::abcd:ab/64',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 6)), output)

    def test_ipv6_multiple_ranges(self):
        input = 'fec::[1-2]bcd:[9-b]/64'
        output = sorted([
            'fec::1bcd:9/64',
            'fec::1bcd:a/64',
            'fec::1bcd:b/64',
            'fec::2bcd:9/64',
            'fec::2bcd:a/64',
            'fec::2bcd:b/64',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 6)), output)

    def test_ipv6_multiple_sets(self):
        input = 'fec::[a,f]bcd:[9,ab]/64'
        output = sorted([
            'fec::abcd:9/64',
            'fec::abcd:ab/64',
            'fec::fbcd:9/64',
            'fec::fbcd:ab/64',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 6)), output)

    def test_ipv6_set_and_range(self):
        input = 'fec::[dead,beaf]:[9-b]/64'
        output = sorted([
            'fec::dead:9/64',
            'fec::dead:a/64',
            'fec::dead:b/64',
            'fec::beaf:9/64',
            'fec::beaf:a/64',
            'fec::beaf:b/64',
        ])

        self.assertEqual(sorted(expand_ipaddress_pattern(input, 6)), output)

    def test_invalid_address_family(self):
        with self.assertRaisesRegex(Exception, 'Invalid IP address family: 5'):
            sorted(expand_ipaddress_pattern(None, 5))

    def test_invalid_non_pattern(self):
        with self.assertRaises(ValueError):
            sorted(expand_ipaddress_pattern('1.2.3.4/32', 4))

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            sorted(expand_ipaddress_pattern('1.2.3.[4-]/32', 4))

        with self.assertRaises(ValueError):
            sorted(expand_ipaddress_pattern('1.2.3.[-4]/32', 4))

        with self.assertRaises(ValueError):
            sorted(expand_ipaddress_pattern('1.2.3.[4--5]/32', 4))

    def test_invalid_range_bounds(self):
        self.assertEqual(sorted(expand_ipaddress_pattern('1.2.3.[4-3]/32', 6)), [])

    def test_invalid_set(self):
        with self.assertRaises(ValueError):
            sorted(expand_ipaddress_pattern('1.2.3.[4]/32', 4))

        with self.assertRaises(ValueError):
            sorted(expand_ipaddress_pattern('1.2.3.[4,]/32', 4))

        with self.assertRaises(ValueError):
            sorted(expand_ipaddress_pattern('1.2.3.[,4]/32', 4))

        with self.assertRaises(ValueError):
            sorted(expand_ipaddress_pattern('1.2.3.[4,,5]/32', 4))

# TODO: alphanumeric
