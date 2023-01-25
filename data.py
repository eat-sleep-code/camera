import json
import os

import globals
from models import CameraControl, CameraControlList, CameraControlGroup, CameraControlGroupList


class Data:
    
    def getCameraControls(): 
        
        with open(os.path.join(globals.appRoot) + 'camera-controls.json') as request:
            data = json.loads(request.read())
            cameraControlGroupList = CameraControlGroupList()
            cameraControlGroupList.cameraControlGroups.clear()
            dataSource = data['controlGroups']

            if len(dataSource) > 0:
                for controlGroupData in dataSource:
                    cameraControlGroup = CameraControlGroup()
                    cameraControlGroup.title = controlGroupData['title']
                    cameraControlList = CameraControlList()
                    cameraControlList.cameraControls.clear()
                    for controlData in controlGroupData['controls']:
                        cameraControl = CameraControl()
                        cameraControl.id = controlData['id']
                        cameraControl.tooltip = controlData['tooltip']
                        cameraControl.icon = controlData['icon']
                        cameraControlList.cameraControls.append(cameraControl)
                    cameraControlGroup.controls = cameraControlList

                    cameraControlGroupList.cameraControlGroups.append(cameraControlGroup)

            return cameraControlGroupList