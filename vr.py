import math
import calca.coord as coord
from calca import symbol
from typing import TypeVar,overload
Pos=TypeVar("Pos")
Pos_Like=TypeVar("Pos_Like")
def overlap2(a:tuple,b:tuple):return (a[0]+b[0],a[1]+b[1])
class VerRect():
    def __init__(self,start:Pos,end:Pos,followable:bool=False):
        self.start=(min(start[0],end[0]),min(start[1],end[1]))
        self.end=(max(start[0],end[0]),max(start[1],end[1]))
        self.followable=followable
        if followable:self.Followed:"dict[str,list[VerRect]]"={}
        self.differed=(self.end[0]-self.start[0],self.end[1]-self.start[1])
    def move(self,x:int,y:int)->Pos_Like:
        self.start=self.start[0]+x,self.start[1]+y
        if self.followable:
            for mode,vrs in self.Followed.items():
                for vr in vrs:vr.move(x,y)
        self.end_redraw()
        return (x,y)
    def absolute(self,x:int=None,y:int=None)->Pos:
        if x is None:x=self.sx
        if y is None:y=self.sy
        differs=(x-self.start[0],y-self.start[1])
        self.start=(x,y)
        if self.followable:
            for mode,vrs in self.Followed.items():
                for vr in vrs:vr.move(*differs)
        self.end_redraw()
        return (x,y)
    def absoluteend(self,x:int=None,y:int=None)->Pos:
        if x is None:x=self.ex
        if y is None:y=self.ey
        return self.absolute(x-self.dx,y-self.dy)
    def expand(self,x:int,y:int=None)->Pos_Like:
        self.bef=self.end
        if y is None:
            try:
                rx,ry=self.ratio(x/self.differed[0]+1)
                for mode,vrs in self.Followed.items():
                    if mode.find("rx") != -1:
                        for vr in vrs:vr.move(rx,0)
                    if mode.find("ry") != -1:
                        for vr in vrs:vr.move(0,ry)
                    if mode.find("x") != -1 and mode.find("rx") == -1:
                        for vr in vrs:vr.expand(rx,0)
                    if mode.find("y") != -1 and mode.find("ry") == -1:
                        for vr in vrs:vr.expand(0,ry)
            except:...
        else:
            self.differed=(self.differed[0]+x,self.differed[1]+y)
            if self.followable:
                for mode,vrs in self.Followed.items():
                    if mode.find("rx") != -1:
                        for vr in vrs:vr.move(x,0)
                    if mode.find("ry") != -1:
                        for vr in vrs:vr.move(0,y)
                    if mode.find("x") != -1 and mode.find("rx") == -1:
                        for vr in vrs:vr.expand(x,0)
                    if mode.find("y") != -1 and mode.find("ry") == -1:
                        for vr in vrs:vr.expand(0,y)
        self.end_redraw()
        return (self.end[0]-self.bef[0],self.end[1]-self.bef[1])
    def ratio(self,r:float)->Pos:
        curend=self.end
        self.differed=(int(self.differed[0]*r),int(self.differed[1]*r))
        self.end_redraw()
        return self.end[0]-curend[0],self.end[1]-curend[1]
    def end_redraw(self):self.end=(self.start[0]+self.differed[0],self.start[1]+self.differed[1])
    def __repr__(self):return str(self.start)+" -> "+str(self.end)
    def __contains__(self,t:"Pos|VerRect"):
        if isinstance(t,VerRect):return self.sx <= t.sx <= self.ex-t.dx and self.sy <= t.sy <= self.ey-t.dy
        else:return self.start[0]<t[0]<self.end[0] and self.start[1]<t[1]<self.end[1]
    def touched(self,vr:"VerRect"):
        return vr.sx-self.dx <= self.sx <= vr.ex and vr.sy-self.dy <= self.sy <= vr.ey
    def edgetouched(self,vr:"VerRect"):
        return math.ceil(vr.sx-self.dx) <= math.ceil(self.sx) <= math.ceil(vr.ex) and math.ceil(vr.sy-self.dy) <= math.ceil(self.sy) <= math.ceil(vr.ey)
    def follows(self,vr:"VerRect",followmode:str="rxry"):
        """Follow Mode
x - Change by the x changes(size change)
y - Same as 'x'
r + x or y - Only changes the place, no size changes."""
        assert vr.followable
        if vr.Followed.get(followmode) is None:vr.Followed[followmode]=[self]
        else:vr.Followed[followmode].append(self)
    def befollowed(self,*vr:"VerRect",followmode:str="rxry"):
        assert self.followable
        if self.Followed.get(followmode) is None:self.Followed[followmode]=list(vr)
        else:self.Followed[followmode]+=list(vr)
    @property
    def rectvalue(self):return self.start+self.differed
    @property
    def lb(self):return (self.start[0],self.end[1])
    @property
    def ru(self):return (self.end[0],self.start[1])
    @property
    def sx(self):return self.start[0]
    @property
    def sy(self):return self.start[1]
    @property
    def ex(self):return self.end[0]
    @property
    def ey(self):return self.end[1]
    @property
    def dx(self):return self.differed[0]
    @property
    def dy(self):return self.differed[1]
    @property
    def xrange(self):return self.start[0],self.end[0]
    @property
    def yrange(self):return self.start[1],self.end[1]
    @property
    def midx(self):return (self.start[0]+self.end[0])/2
    @property
    def midy(self):return (self.start[1]+self.end[1])/2
    @property
    def center(self):return (self.midx,self.midy)
class circle:
    def __init__(self,center:Pos,radius:float):
        self.center=center
        self.centerp=coord.Point(center)
        self.radius=radius
    def move(self,x:int,y:int):self.center=(self.center[0]+x,self.center[1]+y);self.centerp=coord.Point(self.center)
    def absolute(self,x:int,y:int):self.center=x,y
    def expand(self,r:int):self.radius+=r
    def ratio(self,r:"int|float"):self.radius*=r+1
    def touched(self,o:"Pos|circle|VerRect|coord.Point"):
        if isinstance(o,tuple):return coord.Point(o).distance(self.centerp) <= self.radius
        elif isinstance(o,circle):return o.centerp.distance(self.centerp) <= (self.radius+o.radius)
        elif isinstance(o,coord.Point):return o.distance(self.centerp) <= self.radius
        elif isinstance(o,VerRect):
            l1=coord.Line(coord.Segment.connect(o.start,o.ru))
            l2=coord.Line(coord.Segment.connect(o.start,o.lb))
            l3=coord.Line(coord.Segment.connect(o.end,o.ru))
            l4=coord.Line(coord.Segment.connect(o.end,o.lb))
            minlength=min(self.centerp.shortest(l1).Length,self.centerp.shortest(l2).Length,self.centerp.shortest(l3).Length,self.centerp.shortest(l4).Length)
            return minlength <= self.radius or self.centerp.Pos in o
    @property
    def blitcorner(self):return (self.center[0]-self.radius,self.center[1]-self.radius)
    def __contains__(self,o:"Pos|circle|VerRect|coord.Point"):
        if isinstance(o,tuple):return coord.Point(o).distance(self.centerp) <= self.radius
        elif isinstance(o,circle):return o.centerp.distance(self.centerp) <= (self.radius-o.radius)
        elif isinstance(o,coord.Point):return o.distance(self.centerp) <= self.radius
        elif isinstance(o,VerRect):
            l1=coord.Line(coord.Segment.connect(o.start,o.ru))
            l2=coord.Line(coord.Segment.connect(o.start,o.lb))
            l3=coord.Line(coord.Segment.connect(o.end,o.ru))
            l4=coord.Line(coord.Segment.connect(o.end,o.lb))
            minlength=min(self.centerp.shortest(l1).Length,self.centerp.shortest(l2).Length,self.centerp.shortest(l3).Length,self.centerp.shortest(l4).Length)
            return minlength >= self.radius and self.centerp.Pos in o
GRAV=(0,0)
"""Tips: This should be positive let an object to drop to the bottom or right."""
AIRFRICTION=0
"""Tips: This should be positive to decrease flying speed."""
GCON=6.67e-11
SAVING_COMMON=5
def cgGRAV(x:float,y:float):
    """Recommended veritcal GRAV: 1"""
    global GRAV
    GRAV=(x,y)
def cgAIRFRICTION(f:float):
    """Friction can get REALLY big when you have f = 1

Recommended f: 0.05"""
    global AIRFRICTION
    AIRFRICTION=f
def get_gravity()->"tuple[float,float]":global GRAV;return GRAV  
def get_airfriction()->"float":global AIRFRICTION;return AIRFRICTION  
def distance(P1:Pos,P2:Pos)->float:return math.hypot(P1[0]-P2[0],P1[1]-P2[1])
def sgo(start:Pos,end:Pos,realstart:Pos):return realstart[0]+end[0]-start[0],realstart[1]+end[1]-start[1]
class dire:
    def __init__(self,start:Pos, end:Pos, speed:float):
        if speed == 0:raise ValueError("Cannot create no speed direction")
        xshift=end[0]-start[0]
        yshift=end[1]-start[1]
        self.speed=speed
        self.start=start
        self.end=end
        if xshift == 0:
            self.x=0
            self.y=self.speed*symbol(yshift)
        else:
            b=((yshift/xshift) if xshift != 0 else 0)
            self.x=math.sqrt((speed**2)/(b**2+1))*symbol(xshift)
            self.y=b*self.x
        self.angle=math.degrees(math.acos(self.x/speed))
        "The clockwise turn angle from positive x axis"
        if yshift < 0:self.angle=(-self.angle) + 180
        self.s=(self.x,self.y)
        self.sym=(symbol(self.x),symbol(self.y))
    @property
    def ox(self):return self.s[0]
    @property
    def oy(self):return self.s[1]
    @property
    def osx(self):return self.sym[0]
    @property
    def osy(self):return self.sym[1]
    @property
    def ex(self):return self.end[0]
    @property
    def ey(self):return self.end[1]
    @property
    def sx(self):return self.start[0]
    @property
    def sy(self):return self.start[1]
    def turn(self, outend:bool, outstart:bool):
        if outend:self.x, self.y=-abs(self.x)*self.osx,-abs(self.y)*self.osy
        elif outstart:self.x, self.y=abs(self.x)*self.osx,abs(self.y)*self.osy
    def outend(self,r:VerRect):return r.sx*self.osx>=self.ex*self.osx and r.sy*self.osy>=self.ey*self.osy
    def outstart(self,r:VerRect):return r.sx*self.osx<=self.sx*self.osx and r.sy*self.osy<=self.sy*self.osy
    def absolute(self,p:Pos):
        self.end=sgo(self.start,self.end,p)
        self.start=p
    def __str__(self):return "dire(%s, %s, %s)"%(str(self.start),str(self.end),str(self.speed))
class SpVR(VerRect):
    """Subclass of VerRect, provides speed options."""
    def __init__(self,start:Pos,end:Pos,followable:bool=False,gravity:bool=True,density:float=1.0):
        VerRect.__init__(self,start,end,followable)
        self.speed=(0,0)
        self.density=density
        self.xface=self.dy/100
        self.yface=self.dx/100
        self.cgbacc=(0,0)
        self.mass=self.dx*self.dy*self.density
        """In-game switch"""
        self.clearacc=GRAV if gravity else (0,0)
        self.acc=self.clearacc
    @overload
    def cspeed(self,t:"tuple[int,int]",/):...
    @overload
    def cspeed(self,x:int,y:int,/):...
    def cspeed(self,t:"tuple[int,int]|int",y:int=None):
        if y is None:y=t[1];t=t[0]
        self.speed=(self.speed[0]+t,self.speed[1]+y)
    def __add__(self,t:"tuple[int,int]"):self.cspeed(t)
    def __sub__(self,t:"tuple[int,int]"):self.cspeed(-t[0],-t[1])
    def cacc(self,t:"tuple[int,int]|int",y:int=None):
        if y is None:y=t[1];t=t[0]
        self.acc=(self.acc[0]+t,self.acc[1]+y)
    def stop(self,target:Pos_Like=(0,0)):
        self.stopx(target[0])
        self.stopy(target[1])
    def stopx(self,target:float=0):
        self.speed=(target,self.speed[1])
        self.acc=(self.clearacc[0],self.acc[1])
    def stopy(self,target:float=0):
        self.speed=(self.speed[0],target)
        self.acc=(self.acc[0],self.clearacc[1])
    def accless_stopx(self):
        self.speed=(0,self.speed[1])
    def accless_stopy(self):
        self.speed=(self.speed[0],0)
    def acc_stopx(self):
        self.acc=(self.clearacc[0],self.acc[1])
    def acc_stopy(self):
        self.acc=(self.acc[0],self.clearacc[1])
    def keepin(self,vr:"VerRect"):
        '''Keep the rect inside a rect, not getting out.'''
        left=right=up=down=False
        x=True
        if self.sx < vr.sx:self.absolute(vr.sx,self.sy);left=True
        elif vr.ex < self.ex:self.absoluteend(vr.ex,self.ey);right=True
        else:x=False
        if x:self.stopx()
        y=True
        if self.sy < vr.sy:self.absolute(self.sx,vr.sy);up=True
        elif vr.ey < self.ey:self.absoluteend(self.ex,vr.ey);down=True
        else:y=False
        if y:self.stopy()
        return left,right,up,down
    def gravswitch(self,onoff:"bool|None"=None):
        if onoff is None:self.gravity_switch=not self.gravity_switch
        else:self.gravity_switch=onoff
        self.clearacc=GRAV if self.gravity_switch else (0,0)
        self.acc=self.clearacc
    def run_speed(self):
        self.move(*self.speed)
    def run(self):
        """Makes a full operation run"""
        self.cspeed(-self.speed[0]*AIRFRICTION*self.xface,-self.speed[1]*AIRFRICTION*self.yface)
        self.cspeed(overlap2(self.acc,self.cgbacc))
        self.run_speed()
    def clearacce(self):self.acc=self.cgbacc=(0,0)
    def clearveracc(self):self.acc=(self.acc[0],self.clearacc[1])
    @property
    def has_no_speed(self):return self.has_no_verspeed and self.has_no_horispeed
    @property
    def has_no_verspeed(self):return abs(self.speed[1]) <= 0.01
    @property
    def has_no_horispeed(self):return abs(self.speed[0]) <= 0.01
    @property
    def has_no_acc(self):return self.acc == (0,0)
class player_SpVR(SpVR):
    def __init__(self, start: Pos, end: Pos, followable: bool = False, gravity: bool = True, density: float = 1):
        SpVR.__init__(self,start,end,followable,gravity,density)
    def lrudt(self,vr:"VerRect")->"tuple[bool,bool,bool,bool,bool]":
        "left, right, up, down, touch = self.lrudt(vr)"
        return vr.sx - self.dx < self.sx < vr.sx,  vr.ex < self.ex < vr.ex + self.dx,  vr.sy - self.dy < self.sy < vr.sy,  vr.ey < self.ey < vr.ey + self.dy,self.touched(vr)
    def lrudt_olrud(self,vr:"VerRect")->"tuple[bool,bool,bool,bool,bool,bool,bool,bool,bool]":
        left,right,up,down,touch=self.lrudt(vr)
        return left,right,up,down,touch,int(self.end[0])==int(vr.start[0]),int(self.start[0])==int(vr.end[0]),int(self.end[1])==int(vr.start[1]),int(self.start[1])==int(vr.end[1])
    def round_lrudt(self,vr:"VerRect"):
        left,right,up,down,touch = self.lrudt(vr)
        x=y=None
        rx=ry=False
        if left:x=self.end[0]-vr.start[0]
        if right:x=vr.end[0]-self.start[0]
        if up:y=self.end[1]-vr.start[1]
        if down:y=vr.end[1]-self.start[1]
        if x is None and y is not None:ry=True
        elif y is None and x is not None:rx=True
        elif x is y is None:...
        else:
            try:xwent=abs(x/(self.speed[0]-(vr.speed[0] if isinstance(vr,SpVR) else 0)))
            except:xwent=math.inf
            try:ywent=abs(y/(self.speed[1]-(vr.speed[1] if isinstance(vr,SpVR) else 0)))
            except:ywent=math.inf
            rx=xwent<ywent
            ry=ywent<xwent
            if xwent == ywent:rx=ry=True
        return rx,ry
    def stopout(self,vr:"VerRect",extraleft:bool=True,extraright:bool=True,extraup:bool=True,extradown:bool=True)->"tuple[bool,bool,bool,bool]":
        """Return: sides of blocked object (left, right, up ,down)"""
        left,right,up,down,touch,ole,ori,oup,odo=self.lrudt_olrud(vr)
        rx,ry=self.round_lrudt(vr)
        oppspeed=vr.speed if isinstance(vr,SpVR) else (0,0)
        rleft=rright=rup=rdown=False
        if touch:
            lj=self.speed[0] > oppspeed[0] and left and rx
            rj=self.speed[0] < oppspeed[0] and right and rx
            uj=self.speed[1] > oppspeed[1] and up and ry
            dj=self.speed[1] < oppspeed[1] and down and ry
            if not (ole or ori):
                if uj and extraup:
                    self.stopy(oppspeed[1])
                    self.absoluteend(y=vr.start[1])
                    rdown=True
                elif dj and extradown:
                    self.stopy(oppspeed[1])
                    self.absolute(y=vr.end[1])
                    rup=True
            if not (oup or odo):
                if lj and extraleft:
                    self.stopx(oppspeed[0])
                    self.absoluteend(x=vr.start[0])
                    rright=True
                elif rj and extraright:
                    self.stopx(oppspeed[0])
                    self.absolute(x=vr.end[0])
                    rleft=True
        return rleft, rright, rup, rdown