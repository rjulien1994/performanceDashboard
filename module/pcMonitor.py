from module.pcParts import *

class PCmonitor(object):
    def __init__(self):
        pltf = platform.uname()
        
        self.bootTime = psutil.boot_time()
        self.name = f"{pltf.system} {pltf.release}, {pltf.machine}: {pltf.node}"
        
        self.cpu = cpu(psutil, 4)
        self.gpu = gpu(lambda: GPUtil.getGPUs()[0], 0.5)
        self.network = network(psutil.net_io_counters, 4)
        self.ram = memory(lambda: psutil.virtual_memory(), 'RAM', 10)
        self.swap = memory(lambda: psutil.swap_memory(), 'SWAP', 10)
        self.disk = memory(lambda: psutil.disk_usage("C://"), "Disk: C", 0.01)
        
        
    def update(self):
        
        self.gpu.update()#constant update
        self.ram.update()
        self.swap.update()
        self.cpu.update()
        self.network.update()
        self.disk.update()
    
    def convertUnit(self, numBytes):
        U = ['', 'K', 'M', 'G', 'T']
        
        for factor, n in enumerate(U):
            if numBytes < 9*1024/10:
                break   
            else:
                numBytes = round(numBytes/1024,3)
        return numBytes, n+'B'