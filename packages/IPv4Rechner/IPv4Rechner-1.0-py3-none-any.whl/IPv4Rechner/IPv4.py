class IPv4():
    def __init__(self, ip):
        self.ip = ip
    def berechnen(self):
        (addrString, cidrString) = self.ip.split('/')
        addr = addrString.split('.')
        cidr = int(cidrString)
        mask = [0, 0, 0, 0]
        for i in range(cidr):
            mask[i//8] = mask[i//8] + (1 << (7 - i % 8))
        net = []
        for i in range(4):
            net.append(int(addr[i]) & mask[i])
        broad = list(net)
        brange = 32 - cidr
        for i in range(brange):
            broad[3 - i//8] = broad[3 - i//8] + (1 << (i % 8))
        self.netid=".".join(map(str, net))
        self.bcid=".".join(map(str, broad))
        self.masku=".".join(map(str, mask))
        spliteip=self.netid.split(".")
        splitbc=self.bcid.split(".")
        ueip=int(spliteip[3])
        ulep=int(splitbc[3])
        eip=str(ueip+1)
        lep=str(ulep-1)
        self.ersteip=spliteip[0]+"."+ spliteip[1] + "." + spliteip[2] + "." +eip
        self.letzteip=splitbc[0]+"."+ splitbc[1] + "." + splitbc[2] + "." +lep
    def bc(self):
        self.berechnen()
        return(self.bcid)
    def id(self):
        self.berechnen()
        return(self.mask)
    def mask(self):
        self.berechnen()
        return(self.mask)
    def first(self):
        self.berechnen()
        return(self.ersteip)
    def last(self):
        self.berechnen()
        return(self.letzteip)
    def all(self):
        self.berechnen()
        return self.netid,self.ersteip,self.letzteip,self.bcid,self.masku
