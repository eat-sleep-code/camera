class Button(object):
	def __init__(self):
		self.rect = None
		self.text = ''
		self.type = ''
		self.value = ''
		self.icon = ''


# ---------------------------------------------------------------------

class UIItem(object):
	def __init__(self):
		self.id = ''
		self.tooltip = ''
		self.icon = ''

# ---------------------------------------------------------------------

class UIItemList(object):
	def __init__(self):
		self.items = [UIItem()]
	def __iter__(self):
		return iter(self.items)


# ---------------------------------------------------------------------

class UIParent(object):
	def __init__(self):
		self.title = ''
		self.itemList = [UIItemList()]

# ---------------------------------------------------------------------

class UIParentList(object):
	def __init__(self):
		self.parents = [UIParent()]
