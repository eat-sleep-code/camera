import json
import os

import globals
from models import CameraControl, CameraControlList


class Data:
    
    def getControls(): 
        
        with open(os.path.join(globals.appRoot) + 'controls.json') as request:
            data = json.loads(request.read())
            cameraControlList = CameraControlList()
            cameraControlList.controls.clear()
            dataSource = data['controls']

            if len(dataSource) > 0:
                i = 0
                for controlData in dataSource:
                    i = i + 1
                    cameraControl = CameraControl()
                    cameraControl.id = controlData['id']
                    cameraControl.title = controlData['title']
                    cameraControl.icon = controlData['icon']

                    cameraControlList.controls.append(cameraControl)

            return cameraControlList