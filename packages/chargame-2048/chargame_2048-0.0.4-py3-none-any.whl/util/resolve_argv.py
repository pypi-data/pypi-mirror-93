def resolve_argv(argv):
	options = {}
	last_arg = None

	resolved_args = []

	for arg in arv:
		if arg[0:2] == '--':
			arg = arg[2:]
			options[arg] = True
			last_arg = arg

		elif arg[0] == '-':
			for _arg in arg[1:]:
				options[_arg] = True
				last_arg = _arg
		
		else:
			if last_arg:
				options[last_arg] = arg
			else:
				resolved_args.append(arg)

	return resolved_args, options