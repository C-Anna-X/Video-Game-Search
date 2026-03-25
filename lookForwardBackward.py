def lookForwardBackward(currData, currIndex, searchString, searchDirection):
	"""
	Helper function for finding adjacent matches in a list via
	linear search

	Inputs:
		currData: list of data to search in
		currIndex: index of initial seed match
		searchString: string to search for in currData
		searchDirection: integer (1 or -1) indicating either forward or
						 backward search direction

	Returns: list of entries matching 'searchString' in 'currData'
			 either before or after 'currIndex'
	"""

	if searchDirection == -1:
		currIndex -= 1
	else:
		currIndex += 1

	foundMatches = []
	while currIndex >= 0 and currIndex < len(currData):
		currEntry = currData[currIndex]
		if currEntry[0].lower().startswith(searchString.lower()):
			foundMatches.append(currEntry)
			currIndex += searchDirection
		else:
			break

	if searchDirection == -1:
		foundMatches.reverse()

	return foundMatches
