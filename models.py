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
		self.tooltip = ''
		self.icon = ''

# ---------------------------------------------------------------------

class CameraControlList(object):
	def __init__(self):
		self.cameraControls = [CameraControl()]


# ---------------------------------------------------------------------

class CameraControlGroup(object):
	def __init__(self):
		self.title = ''
		self.controls = [CameraControlList()]

# ---------------------------------------------------------------------

class CameraControlGroupList(object):
	def __init__(self):
		self.controlGroups = [CameraControlGroup]
