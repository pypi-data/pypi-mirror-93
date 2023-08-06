_noop = lambda: None

def multi_get_with_default(d: dict):
	def get(*keys, default=None, defaultAction=_noop):
		for key in keys:
			if key in d:
				return d[key]
		
		if default:
			return default
		else:
			return defaultAction()

	return get

