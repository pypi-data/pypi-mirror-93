import threading
import time
from threading import Timer
import ctypes

class ReadOnlyDotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get

    def __setattr__(self, k, v):
        raise RuntimeError('%s is read only' % k)

    def __setitem__(self, k, v):
        raise RuntimeError('%s is read only' % k)


class Device:
    """ Device represesnt a resource
    """

    def __init__(self, dev_info, device_pool, rent_time=120):
        """ init Device

        Args:
            dev_info (dict): device information, must be a dict type
            device_pool (DevicePool): device pool object, used to free resource when don't need resource anymore
            time (int): how long you can possess this resource, in sec
        """
        assert isinstance(dev_info,  ReadOnlyDotDict)

        # save dev related objects
        self._dev_info = dev_info
        self._device_manager = device_pool

        # for record time
        self._rent_time = rent_time
        self._start_time = time.time()

        # start a release timer
        self.thread_id = threading.current_thread().native_id
        self._timer = Timer(rent_time, self._timeout)
        self._timer.name = 'dev-free-timer'
        self._timer.start()

        
    
    def __setattr__(self, name, value):
        """Override the setattr, delegate the attribute with same name as inner ReadOnlyDict setter to readonlydict 

        Args:
            name (str): attribute name to set
            value (any): value to set
        """
        
        if name not in  ['_dev_info', '_device_manager', '_start_time', '_rent_time', '_timer'] and name in self._dev_info.keys():
            self._dev_info.__setitem__(name, value)
        else:
            object.__setattr__(self, name, value)


    def __getattr__(self, name):
        """Override the getattr, so you can access attribute by dot

        Args:
            name (str): attribute name to access

        Returns:
            Any: value
        """
        if name not in  ['_dev_info', '_device_manager', '_start_time', '_rent_time', '_timer'] and name in self._dev_info.keys():
            return self._dev_info.__getattr__(name)
        else:
            raise AttributeError("type object '%s' has no attribute '%s'" % (type(self), name))


    def __del__(self):
        """ free resource when the Device object get freed
        """
        self.free()
        

    def free(self):
        """ free resource activately
        """
        if  self._device_manager != None and self._dev_info != None and self._timer != None:
            self._device_manager._free(self._dev_info)
            self._dev_info = None
            self._device_manager = None
            self._timer.cancel()
            self._timer = None
    
    def _timeout(self):
        """report timeout error
        """
        ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread_id, ctypes.py_object(TimeoutError))

    @property
    def time(self):
        """how much time left before the device will force released

        Returns:
            int: the left time
        """
        left_time =  self._rent_time - (time.time() - self._start_time)

        return int(left_time) if left_time > 0 else 0

class DevicePool:
    """Device Pool

    Device Pool is used to manage resource
    """

    def __init__(self, resource_list):
        """ init device pool
        
        Args:
            resource_list(list): list of dict type, you can save resource information as dict, then pass them as a list of dict to DevicePool 
    """
        for d in resource_list:
            assert type(d) == dict, 'type of element in list must be dict type'
        
        # used to manage availble resource
        self.__available_devices = [ ReadOnlyDotDict(d) for d in resource_list ]
        # used to manage unavaible resource
        self.__unavailable_devices = [ ]


    def get(self, rent_time = 60, filter_func= lambda dev : True, timeout = 0):

        """ allocate reousrce from pool
        
        Args：
            time (int): in sec. how long to rent. if time exceed the rent time, the pool will force release the device
            filter_func (function): used to filter device, so you can get the exact device you want, for example, 'lambda dev: dev.id == 1', you can get the device with id attribute is 1
            timeout (int): in sec. how long do you want to wait, when there is no resource available, default 0 sec
        
        Returns:
            Device: return a device object. if timeout, return None
        """
        assert timeout >= 0, "timeout can't be negtive"
        assert rent_time > 0, "rent time can't less than zero"

        start_time = time.time()
        while True:
            device = list(filter(filter_func, self.__available_devices))
            if len(device) != 0:
                dev = device[0]
                self.__available_devices.remove(dev)
                self.__unavailable_devices.append(dev)

                def force_free():
                    self._free(dev)
                timer = Timer(rent_time, force_free)
                timer.name = 'devpool-free-timer'
                timer.start()
                return Device(dev, self, rent_time=rent_time)
            else:
                wait_time = time.time() - start_time
                if wait_time >= timeout:
                    return None

    @property
    def size(self):
        """the number of  available resources  in the pool
        """
        return len(self.__available_devices)

    def _free(self, dev):
        """free the device you get

        Args:
            dev (ReadOnlyDotDict): device to free
        """
        if dev in self.__unavailable_devices:
            self.__unavailable_devices.remove(dev)
            if dev not in self.__available_devices:
                self.__available_devices.append(dev)


__all__ = [
    
    'DevicePool',
    'Device',
    'ReadOnlyDotDict'
]