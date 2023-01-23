class Button(object):
	def __init__(self):
		self.rect = None
		self.text = ''
		self.type = ''
		self.value = ''
		self.icon = ''


# ---------------------------------------------------------------------

class CameraControl(object):
	def __init__(self):
		self.id = ''
		self.title = ''
		self.icon = ''

# ---------------------------------------------------------------------

class CameraControlList(object):
	def __init__(self):
		self.controls = [Control()]
