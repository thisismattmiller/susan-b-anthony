import requests
import json
import os



todo = []
todo.append('anthony-correspondence')
todo.append('daybook-and-diaries-1856-1906-daybook-1856-1860')
todo.append('daybook-and-diaries-1856-1906-daybook-1865')
todo.append('daybook-and-diaries-1856-1906-daybook-1870')
todo.append('daybook-and-diaries-1856-1906-daybook-1871')
todo.append('daybook-and-diaries-1856-1906-daybook-1872')
todo.append('daybook-and-diaries-1856-1906-daybook-1873')
todo.append('daybook-and-diaries-1856-1906-daybook-1874')
todo.append('daybook-and-diaries-1856-1906-daybook-1876')
todo.append('daybook-and-diaries-1856-1906-daybook-1877')
todo.append('daybook-and-diaries-1856-1906-daybook-1878')
todo.append('daybook-and-diaries-1856-1906-daybook-1883')
todo.append('daybook-and-diaries-1856-1906-daybook-1888')
todo.append('daybook-and-diaries-1856-1906-daybook-1890')

todo.append('daybook-and-diaries-1856-1906-daybook-1893')
todo.append('daybook-and-diaries-1856-1906-daybook-1894')
todo.append('daybook-and-diaries-1856-1906-daybook-1895')
todo.append('daybook-and-diaries-1856-1906-daybook-1896')
todo.append('daybook-and-diaries-1856-1906-daybook-1897')
todo.append('daybook-and-diaries-1856-1906-daybook-1898')
todo.append('daybook-and-diaries-1856-1906-daybook-1899')
todo.append('daybook-and-diaries-1856-1906-daybook-1900')
todo.append('daybook-and-diaries-1856-1906-daybook-1901')
todo.append('daybook-and-diaries-1856-1906-daybook-1903')
todo.append('daybook-and-diaries-1856-1906-daybook-1904')
todo.append('daybook-and-diaries-1856-1906-daybook-1906')

todo.append('anthony-speeches-and-other-writings-list')
todo.append('anthony-speeches-and-other-writings-first-public-address-1848')
todo.append('anthony-speeches-and-other-writings-batavia-1852')
todo.append('anthony-speeches-and-other-writings-liquor-1852')
todo.append('anthony-speeches-and-other-writings-1853')
todo.append('anthony-speeches-and-other-writings-expediency-1853')
todo.append('anthony-speeches-and-other-writings-1856')
todo.append('anthony-speeches-and-other-writings-1858')
todo.append('anthony-speeches-and-other-writings-1859')
todo.append('anthony-speeches-and-other-writings-1861')
todo.append('anthony-speeches-and-other-writings-american-slavery-1861')
todo.append('anthony-speeches-and-other-writings-taney-1861')
todo.append('anthony-speeches-and-other-writings-1862')
todo.append('anthony-speeches-and-other-writings-1877')




for work in todo:

	try:
		os.mkdir(work)
	except:
		pass
		

	url = None
	use_range = []
	if work == 'anthony-correspondence':
		use_range = range(1,228)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-001_00011_00237/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1856-1860':
		use_range = range(1,111)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-001_00239_00348/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1865':
		use_range = range(1,170)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-001_00349_00517/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1870':
		use_range = range(1,165)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-001_00519_00682/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1871':
		use_range = range(1,205)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-001_00683_00886/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1872':
		use_range = range(1,71)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-001_00887_00956/?sp=<COUNTER>&st=text&fo=json'
	if work == 'daybook-and-diaries-1856-1906-daybook-1873':
		use_range = range(1,94)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-002_00008_00105/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1874':
		use_range = range(1,202)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-002_00107_00307/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1876':
		use_range = range(1,101)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-002_00308_00407/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1877':
		use_range = range(1,224)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-002_00409_00631/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1878':
		use_range = range(1,132)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-002_00633_00763/?sp=<COUNTER>&st=text&fo=json'


	if work == 'daybook-and-diaries-1856-1906-daybook-1883':
		use_range = range(1,139)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-002_00764_01001/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1888':
		use_range = range(1,108)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-002_01003_01109/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1890':
		use_range = range(1,217)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-003_00008_00223/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1892':
		use_range = range(1,226)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-003_00225_00449/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1893':
		use_range = range(1,100)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-003_00450_00548/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1894':
		use_range = range(1,218)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-003_00551_00767/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1895':
		use_range = range(1,233)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-003_00768_00999/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1896':
		use_range = range(1,224)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-003_01001_01223/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1897':
		use_range = range(1,224)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-004_00008_00230/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1898':
		use_range = range(1,230)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-004_00231_00459/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1899':
		use_range = range(1,224)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-004_00461_00683/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1900':
		use_range = range(1,222)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-004_00685_00905/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1901':
		use_range = range(1,145)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-004_00906_01049/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1903':
		use_range = range(1,197)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-004_01051_01246/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1904':
		use_range = range(1,150)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-005_00007_00155/?sp=<COUNTER>&st=text&fo=json'

	if work == 'daybook-and-diaries-1856-1906-daybook-1906':
		use_range = range(1,101)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-005_00157_00256/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-list':
		use_range = range(1,3)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-006_00572_00573/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-first-public-address-1848':
		use_range = range(1,13)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-006_00574_00585/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-batavia-1852':
		use_range = range(1,24)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-006_00586_00608/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-liquor-1852':
		use_range = range(1,44)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-006_00609_00651/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-1853':
		use_range = range(1,55)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-006_00652_00705/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-expediency-1853':
		use_range = range(1,53)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-007_00007_00058/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-1856':
		use_range = range(1,56)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-007_00059_00113/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-1858':
		use_range = range(1,48)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-007_00114_00160/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-1859':
		use_range = range(1,22)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-007_00161_00181/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-1861':
		use_range = range(1,18)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-007_00182_00198/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-american-slavery-1861':
		use_range = range(1,7)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-007_00199_00204/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-taney-1861':
		use_range = range(1,24)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-007_00205_00227/?sp=<COUNTER>&st=text&fo=json'

	if work == 'anthony-speeches-and-other-writings-1862':
		use_range = range(1,15)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-007_00228_00241/?sp=<COUNTER>&st=text&fo=json'


	if work == 'anthony-speeches-and-other-writings-1877':
		use_range = range(1,49)
		url = 'https://www.loc.gov/resource/mss11049.mss11049-007_00242_00289/?sp=<COUNTER>&st=text&fo=json'






	for x in use_range:
		print(f"{x}/{len(use_range)}")
		u = url.replace('<COUNTER>',str(x))
		r = requests.get(u)
		if r.status_code == 200:
			json.dump(json.loads(r.text),open(f"{work}/{x}.json",'w'),indent=2)
		else:
			print('eRror on', work, x, f'code: {r.status_code}')
