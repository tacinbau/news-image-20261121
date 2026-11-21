import os,struct,zlib
W=H=1024
px=bytearray(b"\xff")*(W*H)
def rect(x,y,w,h,v=0):
 for j in range(y,y+h):px[j*W+x:j*W+x+w]=bytes([v])*w
def dot(x,y,v=0):
 if 0<=x<W and 0<=y<H:px[y*W+x]=v
def ring(cx,cy,r,v=0):
 x,y,d=0,r,3-2*r
 while x<=y:
  for a,b in((x,y),(y,x),(y,-x),(x,-y),(-x,-y),(-y,-x),(-y,x),(-x,y)):dot(cx+a,cy+b,v)
  x+=1
  if d>0:y-=1;d+=4*(x-y)+10
  else:d+=4*x+6
def frame(x,y,w,h,v=0):
 rect(x,y,w,2,v);rect(x,y+h-2,w,2,v);rect(x,y,2,h,v);rect(x+w-2,y,2,h,v)
def burst(cx,cy,r,v=0):
 ring(cx,cy,r,v);ring(cx,cy,r//2,v)
 rect(cx-r-4,cy-1,2*r+9,2,v);rect(cx-1,cy-r-4,2,2*r+9,v)
 for a,b in((-1,-1),(1,-1),(-1,1),(1,1)):
  for k in range(2,7):dot(cx+a*k,cy+b*k,v)
G={"A":(14,17,17,31,17,17,17),"B":(30,17,17,30,17,17,30),"C":(14,17,16,16,16,17,14),
"D":(30,17,17,17,17,17,30),"E":(31,16,16,30,16,16,31),"F":(31,16,16,30,16,16,16),
"G":(14,17,16,23,17,17,15),"H":(17,17,17,31,17,17,17),"I":(14,4,4,4,4,4,14),
"J":(7,2,2,2,2,18,12),"K":(17,18,20,24,20,18,17),"L":(16,16,16,16,16,16,31),
"M":(17,27,21,21,17,17,17),"N":(17,25,21,19,17,17,17),"O":(14,17,17,17,17,17,14),
"P":(30,17,17,30,16,16,16),"Q":(14,17,17,17,21,18,13),"R":(30,17,17,30,20,18,17),
"S":(15,16,16,14,1,1,30),"T":(31,4,4,4,4,4,4),"U":(17,17,17,17,17,17,14),
"V":(17,17,17,17,17,10,4),"W":(17,17,17,21,21,21,10),"X":(17,17,10,4,10,17,17),
"Y":(17,17,10,4,4,4,4),"Z":(31,1,2,4,8,16,31),"0":(14,17,19,21,25,17,14),
"1":(4,12,4,4,4,4,14),"2":(14,17,1,6,8,16,31),"3":(30,1,1,14,1,1,30),
"4":(2,6,10,18,31,2,2),"5":(31,16,30,1,1,17,14),"6":(6,8,16,30,17,17,14),
"7":(31,1,2,4,8,8,8),"8":(14,17,17,14,17,17,14),"9":(14,17,17,15,1,2,12),
".":(0,0,0,0,0,12,12),",":(0,0,0,0,12,4,8),":":(0,12,12,0,12,12,0),
"-":(0,0,0,14,0,0,0),"%":(25,26,2,4,8,11,19),"(":(2,4,8,8,8,4,2),
")":(8,4,2,2,2,4,8),"'":(4,4,8,0,0,0,0),"$":(4,15,20,14,5,30,4),
"&":(12,18,20,8,21,18,13),"/":(1,2,2,4,8,8,16),"+":(0,4,4,31,4,4,0),
"=":(0,0,31,0,31,0,0),"?":(14,17,1,2,4,0,4),"!":(4,4,4,4,4,0,4),
" ":(0,0,0,0,0,0,0)}
def text(x,y,s,t,v=0):
 for ch in t:
  for r in range(7):
   q=G.get(ch,G[" "])[r]
   for c in range(5):
    if q>>(4-c)&1:rect(x+c*s,y+r*s,s,s,v)
  x+=6*s
 return x
def center(x,y,w,s,t,v=0):text(x+(w-len(t)*6*s+s)//2,y,s,t,v)
def wrap(t,n):
 L=[];c=""
 for x in t.split():
  if c and len(c)+1+len(x)>n:L.append(c);c=x
  elif c:c+=" "+x
  else:c=x
 if c:L.append(c)
 return L
def block(x,y,s,t,n,lh,v=0):
 for l in wrap(t,n):text(x,y,s,l,v);y+=lh
 return y
def chead(x,y,w,s,t,n,lh,v=0):
 for l in wrap(t,n):center(x,y,w,s,l,v);y+=lh
 return y
def chunk(t,d):return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
center(0,18,1024,13,"THE WORLD")
rect(28,120,968,3);rect(28,126,968,1)
center(0,136,1024,3,"SATURDAY, 21 NOVEMBER 2026")
rect(28,166,968,1)
center(0,178,1024,2,"WAR IN EUROPE - AFTER THE SHENZHEN SUMMIT")
chead(28,200,968,4,"MISSILES RAIN ON KYIV, AND FALL IN POLAND",40,32)
block(28,280,2,"RUSSIA FIRED MORE THAN 400 DRONES AND 110 MISSILES AT UKRAINE OVERNIGHT, ONE OF THE LARGEST ATTACKS OF THE WAR. NINE PEOPLE WERE KILLED AND 28 HURT. THREE RUSSIAN OBJECTS THEN LANDED IN POLAND. WARSAW CALLED IT A DELIBERATE PROVOCATION. NO ONE IN POLAND WAS HURT.",46,16)
frame(612,276,384,172)
for bx,bw,bh in((630,40,46),(680,50,66),(740,36,36),(786,44,56),(840,40,41),(890,55,61),(950,30,31)):
 rect(bx,446-bh,bw,bh)
for wx,wy in((640,410),(660,425),(695,400),(705,430),(800,410),(815,425),(905,405),(920,425),(960,425)):
 rect(wx,wy,4,4,255)
burst(655,352,12);burst(760,342,10);burst(915,350,12)
frame(896,284,92,26);center(896,290,92,1,"POLAND")
center(612,452,384,1,"KYIV UNDER FIRE - THE WAR SPILLS OVER")
rect(28,486,968,30,0)
center(28,493,968,2,"400+ DRONES - 110+ MISSILES - 27 BALLISTIC - 9 KILLED, 28 HURT - 3 IN POLAND",255)
rect(28,530,968,2)
chead(28,546,470,3,"AFTER SHENZHEN: PEACE TALK, NO PEACE",26,24)
chead(526,546,470,3,"COURT: MYANMAR COMMITTED GENOCIDE",26,24)
block(28,606,2,"TWO DAYS AFTER TRUMP, XI AND PUTIN SIGNED A PEACE DECLARATION IN SHENZHEN, EUROPE DISMISSED THE SUMMIT AS A PHOTO OP. MOSCOW RULED OUT NATO-STYLE PROTECTION FOR UKRAINE. TRUMP RATED THE MEETING 12 OUT OF 10.",39,16)
block(526,606,2,"THE WORLD COURT RULED 9-6 THAT MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA IN 2017, THE FIRST TIME IT HAS FOUND A STATE GUILTY OF GENOCIDE. BRITAIN EXPELLED MYANMAR'S DEFENCE ATTACHE. ROHINGYA REFUGEES CELEBRATED IN BANGLADESH.",39,16)
rect(511,546,1,156)
rect(28,716,968,2)
chead(28,732,470,3,"UK AND EU REBUILD THE BRIDGES",26,24)
chead(526,732,470,3,"COP31: NO DEAL AS TALKS RUN OVER",26,24)
block(28,792,2,"BRITAIN AND THE EU STRUCK A LANDMARK DEAL IN BRUSSELS: FOOD CHECKS SCRAPPED, EMISSIONS TRADING LINKED, AND 100,000 YOUNG PEOPLE FROM EACH SIDE FREE TO LIVE AND WORK IN THE OTHER FOR UP TO THREE YEARS.",39,16)
block(526,792,2,"CLIMATE TALKS IN ANTALYA SPILLED INTO OVERTIME WITH NO DEAL IN SIGHT. THE LATEST DRAFT DROPS ANY MENTION OF FOSSIL FUELS AND A $120BN ADAPTATION FINANCE TARGET. A NEW TEXT IS DUE ON SATURDAY MORNING. THE US IS ABSENT FOR A SECOND YEAR.",39,16)
rect(511,732,1,156)
rect(28,902,968,2)
rect(28,912,968,78,0)
block(36,918,2,"MARKETS ROUT: S&P 500 -3.70%, NASDAQ -5.28%, NVIDIA SLUMPS ON SEC PROBE REPORT, ANTHROPIC -8.5% TO $88.91 - EU APPROVES 1BN EURO AID FOR UKRAINE - RUTTE DUE IN WARSAW TODAY - IRAN SAYS TWO TANKERS HIT MINES EAST OF HORMUZ",78,16,255)
rect(28,998,968,1)
center(0,1004,1024,1,"THE WORLD - SATURDAY, 21 NOVEMBER 2026 - PAGE 1")
o=os.environ.get("MAKEFUN_OUTPUT_DIR","/output")
os.makedirs(o,exist_ok=True)
a=bytearray()
for i in range(H):a.append(0);a+=px[i*W:(i+1)*W]
open(os.path.join(o,"entry.png"),"wb").write(b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",W,H,8,0,0,0,0))+chunk(b"IDAT",zlib.compress(bytes(a),9))+chunk(b"IEND",b""))
