"""Library tests."""

import base64
from unittest.mock import patch

import pytest

import tplink_ess_lib
from tplink_ess_lib import MissingMac
from tplink_ess_lib.network import InterfaceProblem, Network, ConnectionProblem
from .common import TEST_PACKETS

pytestmark = pytest.mark.asyncio

TEST_HOST_MAC = "00:00:00:00:00:00"
TEST_SWITCH_MAC = "70:4f:57:89:61:6a"


def _get_packets(keys: list[str]):
    """Get packets from the test packets dictionary as a list of tuples with terminating ("","")."""
    return [(TEST_PACKETS[key], "") for key in keys] + [("", "")]


async def test_discovery():
    """Test switch discovery."""
    with patch("tplink_ess_lib.network.socket.socket") as mock_socket:
        mock_socket = mock_socket.return_value
        mock_socket.recvfrom.side_effect = _get_packets(["discovery1"])

        tplink = tplink_ess_lib.TpLinkESS(host_mac=TEST_HOST_MAC, testing=True)

        result = await tplink.discovery()

        # Verify timeout called with proper value
        mock_socket.settimeout.assert_called_with(10)
        # Verify socket bound with proper broadcast address
        mock_socket.bind.assert_called_with(
            (Network.BROADCAST_ADDR, Network.UDP_RECEIVE_FROM_PORT)
        )

        assert result == [
            {
                "dhcp": False,
                "firmware": "1.0.2 Build 20160526 Rel.34684",
                "gateway": "0.0.0.0",
                "hardware": "TL-SG108PE 1.0",
                "hostname": "TL-SG108PE",
                "ip_addr": "192.168.1.3",
                "ip_mask": "255.255.255.0",
                "mac": "18:a6:f7:bc:80:d1",
                "type": "TL-SG108PE",
            }
        ]


async def test_discovery_multi():
    """Test switch discovery with multple switches."""
    with patch("tplink_ess_lib.network.socket.socket") as mock_socket:
        mock_socket = mock_socket.return_value
        mock_socket.recvfrom.side_effect = _get_packets(["discovery1", "discovery2"])

        tplink = tplink_ess_lib.TpLinkESS(host_mac=TEST_HOST_MAC, testing=True)

        result = await tplink.discovery()

        # Verify timeout called with proper value
        mock_socket.settimeout.assert_called_with(10)
        # Verify socket bound with proper broadcast address
        mock_socket.bind.assert_called_with(
            (Network.BROADCAST_ADDR, Network.UDP_RECEIVE_FROM_PORT)
        )

        assert result == [
            {
                "dhcp": False,
                "firmware": "1.0.2 Build 20160526 Rel.34684",
                "gateway": "0.0.0.0",
                "hardware": "TL-SG108PE 1.0",
                "hostname": "TL-SG108PE",
                "ip_addr": "192.168.1.3",
                "ip_mask": "255.255.255.0",
                "mac": "18:a6:f7:bc:80:d1",
                "type": "TL-SG108PE",
            },
            {
                "dhcp": False,
                "firmware": "1.0.0 Build 20160715 Rel.38605",
                "gateway": "192.168.1.4",
                "hardware": "TL-SG105E 3.0",
                "hostname": "switch7",
                "ip_addr": "192.168.1.109",
                "ip_mask": "255.255.255.0",
                "mac": "70:4f:57:89:61:6a",
                "type": "TL-SG105E",
            },
        ]


async def test_stats_query():
    """Test stats query."""
    with patch("tplink_ess_lib.network.socket.socket") as mock_socket:
        mock_socket = mock_socket.return_value
        mock_socket.recvfrom.side_effect = _get_packets(["stats"])

        tplink = tplink_ess_lib.TpLinkESS(host_mac=TEST_HOST_MAC, testing=True)

        result = await tplink.query(TEST_SWITCH_MAC, "stats")

        # Verify timeout called with proper value
        mock_socket.settimeout.assert_called_with(10)
        # Verify socket bound with proper broadcast address
        mock_socket.bind.assert_called_with(
            (Network.BROADCAST_ADDR, Network.UDP_RECEIVE_FROM_PORT)
        )

        assert result == {
            "stats": [
                {
                    "Port": 1,
                    "Status": "Enabled",
                    "Status Raw": 1,
                    "Link Status": "1000Full",
                    "Link Status Raw": 6,
                    "TxGoodPkt": 10085762,
                    "TxBadPkt": 0,
                    "RxGoodPkt": 1062303,
                    "RxBadPkt": 0,
                },
                {
                    "Port": 2,
                    "Status": "Enabled",
                    "Status Raw": 1,
                    "Link Status": "Link Down",
                    "Link Status Raw": 0,
                    "TxGoodPkt": 0,
                    "TxBadPkt": 0,
                    "RxGoodPkt": 0,
                    "RxBadPkt": 0,
                },
                {
                    "Port": 3,
                    "Status": "Enabled",
                    "Status Raw": 1,
                    "Link Status": "1000Full",
                    "Link Status Raw": 6,
                    "TxGoodPkt": 23127099,
                    "TxBadPkt": 0,
                    "RxGoodPkt": 8488829,
                    "RxBadPkt": 0,
                },
                {
                    "Port": 4,
                    "Status": "Enabled",
                    "Status Raw": 1,
                    "Link Status": "Link Down",
                    "Link Status Raw": 0,
                    "TxGoodPkt": 0,
                    "TxBadPkt": 0,
                    "RxGoodPkt": 0,
                    "RxBadPkt": 0,
                },
                {
                    "Port": 5,
                    "Status": "Enabled",
                    "Status Raw": 1,
                    "Link Status": "1000Full",
                    "Link Status Raw": 6,
                    "TxGoodPkt": 9715369,
                    "TxBadPkt": 0,
                    "RxGoodPkt": 25004812,
                    "RxBadPkt": 25,
                },
            ]
        }


async def test_update_data():
    """Test update data function."""
    with patch("tplink_ess_lib.network.socket.socket") as mock_socket:
        mock_socket = mock_socket.return_value

        mock_socket.recvfrom.side_effect = _get_packets(
            [
                "stats",
                "login1",
                "hostname",
                "num_ports",
                "ports",
                "trunk",
                "mtu_vlan",
                "vlan",
                "pvid",
            ]
        )

        tplink = tplink_ess_lib.TpLinkESS(host_mac=TEST_HOST_MAC, testing=True)

        result = await tplink.update_data(switch_mac=TEST_SWITCH_MAC)

        # Verify timeout called with proper value
        mock_socket.settimeout.assert_called_with(10)
        # Verify socket bound with proper broadcast address
        mock_socket.bind.assert_called_with(
            (Network.BROADCAST_ADDR, Network.UDP_RECEIVE_FROM_PORT)
        )

        assert result == {
            "hostname": {
                "type": "TL-SG105E",
                "hostname": "switch7",
                "mac": "70:4f:57:89:61:6a",
                "firmware": "1.0.0 Build 20160715 Rel.38605",
                "hardware": "TL-SG105E 3.0",
                "dhcp": False,
                "ip_addr": "192.168.1.109",
                "ip_mask": "255.255.255.0",
                "gateway": "192.168.1.4",
            },
            "num_ports": {"num_ports": 5},
            "ports": {
                "ports": [
                    "01:01:00:01:06:00:00",
                    "02:01:00:01:00:00:00",
                    "03:01:00:01:06:00:00",
                    "04:01:00:01:00:00:00",
                    "05:01:00:01:06:00:00",
                ]
            },
            "trunk": {"trunk": "01:00:00:00:00"},
            "mtu_vlan": {"mtu_vlan": "00:01"},
            "vlan": {
                "vlan_enabled": "01",
                "vlan": [
                    {
                        "VLAN ID": 1,
                        "Member Ports": "1,2,3,4,5",
                        "Tagged Ports": "",
                        "VLAN Name": "Default_VLAN",
                    },
                    {
                        "VLAN ID": 50,
                        "Member Ports": "1,5",
                        "Tagged Ports": "",
                        "VLAN Name": "GAMING",
                    },
                ],
                "vlan_filler": " ",
            },
            "pvid": {
                "pvid": [(1, 50), (2, 1), (3, 1), (4, 1), (5, 1)],
                "vlan_filler": " ",
            },
        }

        # Test recvfrom socket error
        mock_socket.recvfrom.side_effect = OSError
        with pytest.raises(ConnectionProblem):
            await tplink.update_data(switch_mac=TEST_SWITCH_MAC)


async def test_partial_update_data():
    """Test update data function with subset."""
    with patch("tplink_ess_lib.network.socket.socket") as mock_socket:
        mock_socket = mock_socket.return_value
        mock_socket.recvfrom.side_effect = _get_packets(
            ["login1", "login2", "hostname", "ports"]
        )

        tplink = tplink_ess_lib.TpLinkESS(host_mac=TEST_HOST_MAC, testing=True)

        result = await tplink.update_data(
            switch_mac=TEST_SWITCH_MAC, action_names=["hostname", "ports"]
        )

        assert result == {
            "hostname": {
                "type": "TL-SG105E",
                "hostname": "switch7",
                "mac": "70:4f:57:89:61:6a",
                "firmware": "1.0.0 Build 20160715 Rel.38605",
                "hardware": "TL-SG105E 3.0",
                "dhcp": False,
                "ip_addr": "192.168.1.109",
                "ip_mask": "255.255.255.0",
                "gateway": "192.168.1.4",
            },
            "ports": {
                "ports": [
                    "01:01:00:01:06:00:00",
                    "02:01:00:01:00:00:00",
                    "03:01:00:01:06:00:00",
                    "04:01:00:01:00:00:00",
                    "05:01:00:01:06:00:00",
                ]
            },
        }


async def test_missing_hostmac_exception():
    """Test missing host mac address exception."""
    with pytest.raises(MissingMac):
        tplink_ess_lib.TpLinkESS()


async def test_binding_exceptions():
    """Test socket binding exceptions."""
    with patch("tplink_ess_lib.network.socket.socket") as mock_socket:
        mock_socket = mock_socket.return_value
        mock_socket.bind.side_effect = OSError
        with pytest.raises(OSError):
            tplink = tplink_ess_lib.TpLinkESS(host_mac=TEST_HOST_MAC, testing=True)
            await tplink.discovery()
        mock_socket.bind.side_effect = InterfaceProblem
        with pytest.raises(InterfaceProblem):
            tplink = tplink_ess_lib.TpLinkESS(host_mac=TEST_HOST_MAC, testing=True)
            await tplink.discovery()
        mock_socket.bind.side_effect = InterfaceProblem
        with pytest.raises(InterfaceProblem):
            tplink = tplink_ess_lib.TpLinkESS(host_mac=TEST_HOST_MAC)
            await tplink.update_data(switch_mac=TEST_SWITCH_MAC)
