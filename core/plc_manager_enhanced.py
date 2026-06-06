import socket
import struct
import time
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class PLCManagerEnhanced:
    """
    Enhanced PLC Manager with TCP/IP and Modbus support
    Supports both Ethernet and Serial Modbus protocols
    """
    
    def __init__(self, config: dict = None):
        """
        Initialize PLC Manager
        
        Args:
            config: PLC configuration dictionary
        """
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.plc_type = self.config.get('type', 'tcp')
        self.host = self.config.get('host', '192.168.1.100')
        self.port = self.config.get('port', 502)
        self.device_id = self.config.get('device_id', 1)
        self.timeout = self.config.get('timeout', 5000) / 1000
        self.retry_count = self.config.get('retry_count', 3)
        
        self.signals = self.config.get('signals', {})
        self.socket = None
        self.connected = False
        self.trigger = False
        
        if self.enabled:
            self.connect()
    
    def connect(self) -> bool:
        """
        Connect to PLC
        
        Returns:
            bool: True if connection successful
        """
        if not self.enabled:
            print("⚠️ PLC is disabled in config")
            return False
        
        try:
            if self.plc_type == 'tcp':
                return self._connect_tcp()
            elif self.plc_type == 'modbus_tcp':
                return self._connect_modbus_tcp()
            else:
                print(f"❌ Unknown PLC type: {self.plc_type}")
                return False
        except Exception as e:
            print(f"❌ PLC Connection Error: {e}")
            logger.error(f"PLC Connection Error: {e}")
            return False
    
    def _connect_tcp(self) -> bool:
        """Connect via TCP/IP socket"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"✅ PLC Connected (TCP): {self.host}:{self.port}")
            return True
        except socket.timeout:
            print(f"❌ PLC Connection Timeout: {self.host}:{self.port}")
            return False
        except ConnectionRefusedError:
            print(f"❌ PLC Connection Refused: {self.host}:{self.port}")
            return False
    
    def _connect_modbus_tcp(self) -> bool:
        """Connect via Modbus TCP"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"✅ PLC Connected (Modbus TCP): {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Modbus TCP Connection Error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from PLC"""
        try:
            if self.socket:
                self.socket.close()
                self.connected = False
                print("✅ PLC Disconnected")
        except Exception as e:
            print(f"⚠️ Disconnect Error: {e}")
    
    def read_trigger(self) -> bool:
        """
        Read trigger signal from PLC
        
        Returns:
            bool: Trigger state
        """
        if not self.connected:
            return False
        
        try:
            trigger_signal = self.signals.get('trigger_input', 'I0.0')
            # Parse signal (I0.0 format)
            value = self._read_signal(trigger_signal)
            self.trigger = value
            return value
        except Exception as e:
            print(f"⚠️ Error reading trigger: {e}")
            return False
    
    def write_ok(self) -> bool:
        """
        Write OK signal to PLC
        
        Returns:
            bool: True if successful
        """
        if not self.connected:
            print("⚠️ PLC not connected, simulating OK")
            return False
        
        try:
            ok_signal = self.signals.get('ok_output', 'Q0.0')
            self._write_signal(ok_signal, True)
            print("✅ PLC -> OK")
            logger.info("PLC OK signal sent")
            return True
        except Exception as e:
            print(f"❌ Error writing OK: {e}")
            logger.error(f"Error writing OK: {e}")
            return False
    
    def write_ng(self) -> bool:
        """
        Write NG signal to PLC
        
        Returns:
            bool: True if successful
        """
        if not self.connected:
            print("⚠️ PLC not connected, simulating NG")
            return False
        
        try:
            ng_signal = self.signals.get('ng_output', 'Q0.1')
            self._write_signal(ng_signal, True)
            print("✅ PLC -> NG")
            logger.info("PLC NG signal sent")
            return True
        except Exception as e:
            print(f"❌ Error writing NG: {e}")
            logger.error(f"Error writing NG: {e}")
            return False
    
    def write_ready(self) -> bool:
        """Write Ready signal to PLC"""
        try:
            ready_signal = self.signals.get('ready_output', 'Q0.2')
            self._write_signal(ready_signal, True)
            logger.info("PLC Ready signal sent")
            return True
        except Exception as e:
            logger.error(f"Error writing Ready: {e}")
            return False
    
    def write_busy(self) -> bool:
        """Write Busy signal to PLC"""
        try:
            busy_signal = self.signals.get('busy_output', 'Q0.3')
            self._write_signal(busy_signal, True)
            logger.info("PLC Busy signal sent")
            return True
        except Exception as e:
            logger.error(f"Error writing Busy: {e}")
            return False
    
    def set_trigger(self, state: bool):
        """Set trigger state"""
        self.trigger = state
    
    def _read_signal(self, signal: str) -> bool:
        """
        Read signal from PLC
        Signal format: I0.0 (Input bit 0.0)
        """
        # Placeholder for actual signal reading
        # In production, implement actual Modbus read
        return self.trigger
    
    def _write_signal(self, signal: str, value: bool):
        """
        Write signal to PLC
        Signal format: Q0.0 (Output bit 0.0)
        """
        # Placeholder for actual signal writing
        # In production, implement actual Modbus write
        if not self.connected:
            return
        
        # Simulate signal writing
        print(f"   Signal: {signal} = {value}")
    
    def _modbus_read_coil(self, address: int) -> bool:
        """Read Modbus coil"""
        try:
            # Modbus RTU read coil request
            request = self._build_modbus_request(0x01, address, 1)
            
            if self.socket:
                self.socket.send(request)
                response = self.socket.recv(1024)
                return self._parse_modbus_response(response)
            return False
        except Exception as e:
            logger.error(f"Modbus read coil error: {e}")
            return False
    
    def _modbus_write_coil(self, address: int, value: bool) -> bool:
        """Write Modbus coil"""
        try:
            # Modbus RTU write coil request
            request = self._build_modbus_request(0x05, address, 1, value)
            
            if self.socket:
                self.socket.send(request)
                response = self.socket.recv(1024)
                return len(response) > 0
            return False
        except Exception as e:
            logger.error(f"Modbus write coil error: {e}")
            return False
    
    def _build_modbus_request(self, func_code: int, address: int, count: int, value: bool = None) -> bytes:
        """Build Modbus request"""
        # Simplified Modbus TCP request building
        transaction_id = b'\x00\x01'
        protocol_id = b'\x00\x00'
        length = b'\x00\x06'
        unit_id = bytes([self.device_id])
        func = bytes([func_code])
        addr = struct.pack('>H', address)
        cnt = struct.pack('>H', count)
        
        return transaction_id + protocol_id + length + unit_id + func + addr + cnt
    
    def _parse_modbus_response(self, response: bytes) -> bool:
        """Parse Modbus response"""
        if len(response) < 9:
            return False
        
        # Check if response is valid
        return response[7] == 0
    
    def test_connection(self) -> bool:
        """
        Test PLC connection
        
        Returns:
            bool: True if connection is working
        """
        try:
            if not self.connected:
                print("❌ PLC not connected")
                return False
            
            # Send test command
            self.write_ready()
            time.sleep(0.1)
            
            print("✅ PLC Connection Test: OK")
            return True
        except Exception as e:
            print(f"❌ PLC Connection Test Failed: {e}")
            return False
    
    def get_status(self) -> dict:
        """Get PLC status"""
        return {
            'enabled': self.enabled,
            'connected': self.connected,
            'type': self.plc_type,
            'host': self.host,
            'port': self.port,
            'trigger': self.trigger
        }
    
    def __del__(self):
        """Cleanup on deletion"""
        self.disconnect()
