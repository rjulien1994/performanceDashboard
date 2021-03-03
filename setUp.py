from module.pcMonitor import *
from module.dashboard import *

#We create the pc monitor and dashboard separetly
pc = PCmonitor()
dash = dashboard('PC Dashboard', [800,450])

#We add the elements we want on the dashboard and link the value to be associated
dash.addElem('CPUMeter', [30,42], meterIcon([350,350],'CPU', '%', 
                                             labels=[0, 20, 40, 60, 80, 100], subLabel=3,
                                             rotRange=[7*math.pi/4, math.pi/4],
                                             color=(0,50,250), 
                                             labelColor=[(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)],
                                             fontColor=(255,255,255)),
             value = lambda: pc.cpu('load')
            )

dash.addElem('core1Meter', [23,32], meterIcon([70,70],'1', '', 
                                             labels=[0, ''], subLabel=7,
                                             rotRange=[2*math.pi, 0],
                                             color=(0,150,150), 
                                             labelColor=[(0,255,0),(255,0,0)],
                                             fontColor=(255,255,255)),
             value = lambda: pc.cpu('coresLoad')[0]
            )
dash.addElem('core2Meter', [37,32], meterIcon([70,70],'2', '', 
                                             labels=[0, ''], subLabel=7,
                                             rotRange=[2*math.pi, 0],
                                             color=(0,150,150), 
                                             labelColor=[(0,255,0),(255,0,0)],
                                             fontColor=(255,255,255)),
             value = lambda: pc.cpu('coresLoad')[1]
            )

dash.addElem('core3Meter', [23,48], meterIcon([70,70],'3', '', 
                                             labels=[0, ''], subLabel=7,
                                             rotRange=[2*math.pi, 0],
                                             color=(0,150,150), 
                                             labelColor=[(0,255,0),(255,0,0)],
                                             fontColor=(255,255,255)),
             value = lambda: pc.cpu('coresLoad')[2]
            )

dash.addElem('core4Meter', [37,48], meterIcon([70,70],'4', '', 
                                             labels=[0, ''], subLabel=7,
                                             rotRange=[2*math.pi, 0],
                                             color=(0,150,150), 
                                             labelColor=[(0,255,0),(255,0,0)],
                                             fontColor=(255,255,255)),
             value = lambda: pc.cpu('coresLoad')[3]
            )
1
dash.addElem('netDown', [30,70], lcdIcon('D', [110, 23], [50, 55], color=(0,175,255),fontColor=(10,10,10)), value = lambda: pc.convertUnit(pc.network('downRate')))
dash.addElem('netUp', [30,65], lcdIcon('U', [110, 22], [50, 55], color=(0,175,255),fontColor=(10,10,10)), value = lambda: pc.convertUnit(pc.network('upRate')))

dash.addElem('ramMeter', [16,71], meterIcon([180,180],'RAM', 'GB', 
                                             labels=[0, 4,8,12,16], subLabel=1,
                                             rotRange=[math.pi/4, -3*math.pi/4],
                                             color=(0,150,150), 
                                             labelColor=[(0,255,0),(55,200,0),(155,155,0),(200,50,0),(255,0,0)],
                                             fontColor=(255,255,255), outline=False),
            value = lambda: pc.ram('load')
            )

dash.addElem('swapMeter', [44,71], meterIcon([180,180],'SWAP', 'GB', 
                                             labels=[0, 8, 16, 24, 32], subLabel=1,
                                             rotRange=[3*math.pi/4, -math.pi/4],
                                             color=(0,150,150), 
                                             labelColor=[(0,255,0),(55,200,0),(155,155,0),(200,50,0),(255,0,0)],
                                             fontColor=(255,255,255), outline=False),
            value = lambda: pc.swap('load')
            )

dash.addElem('GPUMeter', [70,42], meterIcon([350,350],'GPU', '%', 
                                             labels=[0, 20, 40, 60, 80, 100], subLabel=3,
                                             rotRange=[7*math.pi/4, math.pi/4],
                                             color=(0,50,250), 
                                             labelColor=[(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)],
                                             fontColor=(255,255,255)),
             value = lambda: pc.gpu('load')
            )

dash.addElem('GPUMemMeter', [70,65], meterIcon([120,120],'Memory', 'GB', 
                                             labels=[0, 3, 6], subLabel=1,
                                             rotRange=[7*math.pi/4, math.pi/4],
                                             color=(0,50,250), 
                                             labelColor=[(0,255,0),(255,255,0), (255,0,0)],
                                             fontColor=(255,255,255)),
             value = lambda: pc.gpu('memLoad')
            )

dash.addElem('GPUTemp', [77, 33], indicatorIcon('top', [50,50], "img/coolIcon.png"),value = lambda: pc.gpu('temperature')>70)

dash.addElem('diskMeter', [83,77], meterIcon([250,250],'Disk C', 'TB', 
                                             labels=[1, 0], subLabel=3,
                                             rotRange=[3*math.pi/4, math.pi/4],
                                             color=(0,50,250), 
                                             labelColor=[(0,255,0),(255,0,0)],
                                             fontColor=(255,255,255), outline=False),
             value = lambda: pc.disk('load')
            )