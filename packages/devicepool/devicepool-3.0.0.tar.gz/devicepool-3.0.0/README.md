# changelist
* 3.0.0,  add force free: when time is up, the subthread in Device and DevicePool will free resource automatically
* 2.3.2,  update readme
* 2.3.1,  add free function for Device, so you can free Device by call free()
* 2.3.0,  add size property for DevicePool, so you can know how many available resources in the pool
* 2.2.2,  fix readme problem
* 2.2.1,  fix readme problem
* 2.2.0,  make device returned by devicepool writtable but can modify the attribute assigned from DevicePool
* 2.1.0,  make device returned by devicepool readonly

# feedback
* send email to dvdface@gmail.com
* visit https://github.com/dvdface/devicepool

# how to install
`pip install devicepool`

# how to use
1. import library first
`from devicepool import Device, DevicePool`
2. make a resource dict list
	```
	resource_list = [
		{
			'ip':	'192.168.1.1',
			'type': 'android'
		},
		
		{
			'ip':	'192.168.1.2',
			'type': 'ios'
		}
	]
	```
3. init devicepool
	```
	devicepool = DevicePool(resource_list)
	```
4. get a device from the pool
	```
	# know how many available resource in the pool
	devicepool.size
	
	# allocate any dev from resource pool
	dev = devicepool.get()

	# use filter_func to get desired resource, for exmaple type == 'android'
	dev = devicepool.get(filter_func=lambda dev: dev.type == 'android')

	# use timeout to wait, default timeout is zero
	dev = devicepool.get(timeout=10)
	```
5. check if allocating device is successfully
	```
	# if resource is not enougth and timeout, return None
	# so you need check if dev is None
	if dev == None:
		print('allocate resource failed')
	```
6. use the device by dot way
	```
	print(dev.ip)
	print(dev.type)
	```
7. free the device, or let't it free automatically
	```
	dev.free()
	```