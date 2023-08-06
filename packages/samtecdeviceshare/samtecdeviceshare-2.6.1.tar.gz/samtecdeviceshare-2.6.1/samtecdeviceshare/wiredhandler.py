""" Wired Network Handler """
#!/usr/bin/env python
from enum import Enum
import re
import os
import copy
import time
import logging
from asyncio import CancelledError
from typing import Optional, Pattern, Union
import humps
from pydantic import BaseModel  # pylint: disable=no-name-in-module

logger = logging.getLogger('sdc.wirednetwork')

try:
    import NetworkManager as NM  # type: ignore
except Exception as err:
    if os.getenv('PYTHON_ENV') == 'development':
        logger.warning('Failed to load NetworkManager. Using emulator in development.')
    else:
        logger.warning('Failed to load NetworkManager module.')
    class NetworkManager:
        @classmethod
        def GetDevices(cls):
            return []
        ActiveConnections = []
        @classmethod
        def ActivateConnection(cls, *args, **kwargs):
            pass
    class NetworkManagerModule:
        NM_DEVICE_STATE_ACTIVATED = 100
        NM_DEVICE_STATE_IP_CHECK = 80
        NM_DEVICE_STATE_IP_CONFIG = 70
        NM_DEVICE_STATE_FAILED = 120
        NM_DEVICE_STATE_UNAVAILABLE = 20
        NM_DEVICE_STATE_UNMANAGED = 10
        NM_DEVICE_TYPE_ETHERNET = 1
        NetworkManager = NetworkManager
        @classmethod
        def nm_state(cls):
            pass
    NM = NetworkManagerModule

class CamelModel(BaseModel):
    class Config:
        alias_generator = humps.camelize
        allow_population_by_field_name = True

class WiredConnectionMethod(str, Enum):
    disabled = 'disabled'
    auto = 'auto'
    link_local = 'link-local'
    manual = 'manual'

class WiredConnectionState(str, Enum):
    DISCONNECTED = 'DISCONNECTED'
    CONNECTING = 'CONNECTING'
    CONNECTED = 'CONNECTED'

class WiredNetworkConfig(CamelModel):
    iface: Optional[str] = None
    iface_regex: Optional[Pattern] = None
    method: WiredConnectionMethod = WiredConnectionMethod.auto
    timeout: float = 15
    fallback: Optional[WiredConnectionMethod] = None
    fallback_timeout: float = -1

class WiredConnectionFsm(CamelModel):
    dev_iface: str = ''
    dev_state: int = NM.NM_DEVICE_STATE_UNAVAILABLE
    con_name: Optional[str] = None
    con_state: str = WiredConnectionState.DISCONNECTED
    con_method: WiredConnectionMethod = WiredConnectionMethod.disabled
    con_counter: int = 0
    con_needs_init: bool = True

def get_wired_device(iface: Optional[Union[Pattern,str]] = None):
    for dev in NM.NetworkManager.GetDevices():
        if dev.DeviceType != NM.NM_DEVICE_TYPE_ETHERNET:
            continue
        if iface is None:
            return dev
        if isinstance(iface, re.Pattern) and iface.fullmatch(dev.Interface):
            return dev
        if isinstance(iface, str) and iface == dev.Interface:
            return dev
    return None

def get_active_wired_connection(iface: Optional[Union[Pattern,str]] = None, con_name: Optional[str] = None):
    for act in NM.NetworkManager.ActiveConnections:
        try:
            settings = act.Connection.GetSettings()
            act_devs = act.Devices
            # Skip if connection isnt 802-3-ethernet or no devices attached
            if settings['connection'].get('type') != '802-3-ethernet' or '802-3-ethernet' not in settings or not act_devs:
                continue

            if isinstance(iface, re.Pattern):
                found_dev = next((d for d in act_devs if iface.fullmatch(d.Interface)), None)
                if not found_dev:
                    continue
                return act.Connection, found_dev
            if isinstance(iface, str):
                found_dev = next((d for d in act_devs if d.Interface == iface), None)
                if not found_dev:
                    continue
                return act.Connection, found_dev
            if con_name:
                if con_name != settings.get('connection', {}).get('id', ''):
                    continue
                return act.Connection, act_devs[0]
            # If no input, pick first dev
            return act.Connection, act_devs[0]
        except Exception as err:
            logger.warning('Skipping active connection. Failed parsing with error: %s', err)
    return None, None

def update_active_wired_connection(con=None, dev=None, method: WiredConnectionMethod = WiredConnectionMethod.auto):
    success = False
    try:
        settings = con.GetSettings()
        # Add IPv4 setting if it doesn't yet exist
        if 'ipv4' not in settings:
            settings['ipv4'] = {}
        # Set the method and change properties
        settings['ipv4']['method'] = method.value
        settings['ipv4']['addresses'] = []
        con.Update(settings)
        con.Save()
        NM.NetworkManager.ActivateConnection(con, dev, "/")
        success = True
    except Exception:
        success = False
    return success

class WiredNetworkHandler:
    NM_CONNECTED_STATES = [NM.NM_DEVICE_STATE_ACTIVATED]
    NM_CONNECTING_STATES = [
        NM.NM_DEVICE_STATE_IP_CHECK,
        NM.NM_DEVICE_STATE_IP_CONFIG
    ]
    NM_DISCONNECTED_STATES = [
        NM.NM_DEVICE_STATE_FAILED,
        NM.NM_DEVICE_STATE_UNAVAILABLE,
        NM.NM_DEVICE_STATE_UNMANAGED
    ]

    def __init__(self, config: WiredNetworkConfig):
        self.config = config
        self.fsm = WiredConnectionFsm(con_method=self.config.method)

    def update(self):

        if os.getenv('PYTHON_ENV') == 'development':
            # logger.debug('WIRED %s updating...', self.config.iface_regex or self.config.iface)
            return

        next_fsm = copy.deepcopy(self.fsm)

        # Get active connection and device
        con, dev = get_active_wired_connection(iface=self.config.iface_regex or self.config.iface, con_name=self.fsm.con_name)
        if dev is None:
            dev = get_wired_device(iface=self.config.iface_regex or self.config.iface)

        # If no conn or no device, then treat as unplugged (requires initializing)
        if dev is None or con is None:
            logger.debug('No ethernet device found for %s. Sleeping...', self.config.iface_regex or self.config.iface)
            next_fsm.dev_iface = dev.Interface if dev else self.config.iface
            next_fsm.dev_state = dev.State if dev else NM.NM_DEVICE_STATE_UNAVAILABLE
            next_fsm.con_name = None
            next_fsm.con_method = self.config.method
            next_fsm.con_counter = 0
            next_fsm.con_needs_init = True
            self.fsm = next_fsm
            return # Nothing to do

        # Both connection and device exist, update state
        con_settings = con.GetSettings()
        con_method = WiredConnectionMethod(con_settings.get('ipv4', {}).get('method', self.config.method.value))

        # If method doesnt match, NM is using file config which is different than specified.
        # Need to change method and re-initialize process
        if con_method not in (self.config.method, self.config.fallback):
            logger.warning('Wired device connection method doesnt match. Reinitialzing...')
            con_method = self.config.method
            next_fsm.con_counter = 0
            next_fsm.con_needs_init = True

        next_fsm.con_name = con_settings.get('connection', {}).get('id', '')
        next_fsm.dev_iface = dev.Interface
        next_fsm.dev_state = dev.State

        # CONNECTED
        if next_fsm.dev_state in WiredNetworkHandler.NM_CONNECTED_STATES:
            next_fsm.con_counter = 0
            next_fsm.con_state = WiredConnectionState.CONNECTED
            next_fsm.con_method = con_method

        # CONNECTING
        elif next_fsm.dev_state in WiredNetworkHandler.NM_CONNECTING_STATES:
            next_fsm.con_state = WiredConnectionState.CONNECTING
            # primary method timeout, go to fallback
            if con_method == self.config.method and next_fsm.con_counter >= self.config.timeout:
                logger.info('Primary method timeout- switching to fallback')
                next_fsm.con_method = self.config.fallback if self.config.fallback and self.config.fallback_timeout > 0 else self.config.method
                next_fsm.con_counter = 0
            # fallback timeout, go to primary
            elif con_method == self.config.fallback and next_fsm.con_counter >= self.config.fallback_timeout:
                logger.info('Fallback method timeout- switching back to primary')
                next_fsm.con_method = self.config.method
                next_fsm.con_counter = 0
            # Still trying to connect
            else:
                next_fsm.con_method = con_method
                next_fsm.con_counter += 1

        # DISCONNECTED
        elif next_fsm.dev_state in WiredNetworkHandler.NM_DISCONNECTED_STATES:
            next_fsm.con_counter = 0
            next_fsm.con_state = WiredConnectionState.DISCONNECTED
            next_fsm.con_method = self.config.method
        else:
            next_fsm.con_method = con_method

        if next_fsm.dev_iface != self.fsm.dev_iface:
            logger.info('Wired device iface changed to {0}'.format(next_fsm.dev_iface))
        if next_fsm.con_name != self.fsm.con_name:
            logger.info('Wired connection name changed to {0}'.format(next_fsm.con_name))
        if next_fsm.con_state != self.fsm.con_state:
            logger.info('Wired connection state changed to {0}'.format(next_fsm.con_state))

        # If have connection and want method to change or needs initialization
        if next_fsm.con_needs_init or (next_fsm.con_method != con_method):
            # IMPORTANT: On init we must start with primary method
            next_con_method = self.config.method if next_fsm.con_needs_init else next_fsm.con_method
            logger.info('Setting connection {0} to method {1}'.format(next_fsm.con_name, next_con_method))
            success = update_active_wired_connection(con, dev, next_con_method)
            # NOTE: If failed to activate, restart process
            if not success:
                next_fsm.con_needs_init = True
                logger.error('Failed setting active connection method.')
            else:
                next_fsm.con_needs_init = False
                logger.info('Successfully set active connection method.')
        self.fsm = next_fsm

def run(config: WiredNetworkConfig):
    try:
        handler = WiredNetworkHandler(config)
        while True:
            handler.update()
            time.sleep(1)
    except CancelledError:
        logger.warning('Process cancelled by task. Shutting down...')
    except KeyboardInterrupt:
        logger.warning('Process cancelled by user. Shutting down...')
    except Exception as err:
        logger.exception(err)
        raise err

if __name__ == '__main__':
    run(WiredNetworkConfig())
