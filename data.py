import json
import os

import globals
from models import UIItem, UIItemList, UIParent, UIParentList


class Data:
    
    def getControls(): 
        
        with open(os.path.join(globals.appRoot) + 'camera-controls.json') as request:
            data = json.loads(request.read())
            uiParentList = UIParentList()
            uiParentList.parents.clear()
            dataSource = data['controlGroups']

            if len(dataSource) > 0:
                for parent in dataSource:
                    uiParent = UIParent()
                    uiParent.title = parent['title']

                    # Get child controls
                    uiItemList = UIItemList()
                    uiItemList.items.clear()
                    for item in parent['controls']:
                        uiItem = UIItem()
                        uiItem.id = item['id']
                        uiItem.tooltip = item['tooltip']
                        uiItem.icon = item['icon']
                        uiItemList.items.append(uiItem)
                    
                    # Append child controls to parent group
                    uiParent.itemList = uiItemList
                    uiParentList.parents.append(uiParent)
            
            return uiParentList