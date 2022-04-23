import random
weapon=int(input("Number of Weapons "))
target= int(input("Number of Targets "))
minMenzil=int(input("Güvenlik menzili "))
#selfdefense=int(input("Özemniyet menzili "))

v=int(input("Füze hızı "))
values=[]
pk=[]
#v=1000
#minMenzil=2



for i in range(target):
    values.append(random.randint (60,100))


for i in range(weapon):
    pk.append(random.randint (80,100)/100)

setup=[]
toplamSetup=0
for i in range(target+1):
    satir=[]
    for j in range(target+1):
        if (i==j):
            satir.append(-1)
        rndSetup=random.randint(10,100)/20
        satir.append(rndSetup)
        toplamSetup += rndSetup
    setup.append(satir)
#print("setup", setup)

distances=[]

for i in range(target):
    distances.append(random.randint(int(int(minMenzil)/10),int(minMenzil)*20))
'''
setup=[ [-1,6,7,8,3,1],
    [9,-1,7,5,2,6],
    [6,7,-1,5,1,7],
    [7,7,5,-1,2,8],
    [5,5,5,2,-1,3],
    [2,1,2,3,1,-1]]
'''
goallist=[]
goals=[]
goallist.append("! this problem is generated randomly for "+str(target)+ "number of targets and "+str(weapon)+"number of weapons.;")
goallist.append("! xij: i weapon index, j target index if the weapon i is fired to target j xij =1 else xij=0;")


for j in range(target):
    goal = ""
    for i in range(weapon):
        r="*"
        goal += "(1-"+str(pk[i])+")^x"+str(i+1)+"_"+str(j+1)+r

    goal=goal[:-1]
    goal ="("+str(1)+"-"+goal+")"
    goals.append(goal)

goal ="pK="
for i in goals:
    goal +=i +"+"

goal = goal.rstrip(goal[-1])
goalA=goal+";";
#goal = goal +"-stp;"
goal="pK/"+str(target)+"-"+"stp/"+str(round(toplamSetup,3))+";"

goallist.append("max ="+goal)
goallist.append(goalA)
# const G1
constraints =[]

if (target < weapon):
    constraints.append("! Grup 1: Bir füze bir hedefe atılır ;")
else:
    constraints.append("! Grup 1: Bir füze bir füze atılır veya atılmaz;")

for i in range(weapon):
    cnst= ""
    for j in range(target):
        if (j==target-1):
            r=""
        else:
            r="+"

        ara="*("
        for k in range(target+1):
            if k==j+1:
                continue
            ara +="h"+str(k)+"_"+str(j+1) + "+"
        l = len(ara)

        ara = ara[:l - 1]

        ara+=")"

        cnst +="x"+str(i+1)+"_"+str(j+1) +r#+ara+r
    sgn="<=1"
    if (target<weapon):
        sgn="<="
        vl ="1"
    else:
        sgn ="<="
        vl="1"

    cnst +=sgn+vl
    constraints.append(cnst+";")

if (target < weapon):
    constraints.append("! Grup 2: Bir hedefe sıfır veya birden fazla füze atılabilir ;")
else:
    constraints.append("! Grup 2: Bir hedefe bir veya sıfır füze ateşlenebilir;")

for i in range(target):
    cnst= ""
    for j in range(weapon):
        if (j==weapon-1):
            r=""
        else:
            r="+"

        cnst +="x"+str(j+1)+"_"+str(i+1) +r
    sgn="="
    if (weapon<target):
        sgn="<="
        vl="y"+str(i)
    else: # (weapon>=target):
        sgn =">="
        vl="y"+str(i)

    cnst +=sgn+vl
    constraints.append(cnst+";")
constraints.append("M=9999999999999999;")
constraints.append("! Grup 3: Toplam mühimmat kısıtı;")
cnst = ""

for i in range(target):

    for j in range(weapon):
        cnst +="x"+str(j+1)+"_"+str(i+1) +"+"

l = len(cnst)

cnst = cnst[:l - 1]
cnst +="<="+str(weapon)+";"
constraints.append(cnst)
 ###

constraints.append("! Grup 4: Güvenlik Menzili içinde kalan hedefe ateş edilmeme kısıtları;")
for i in range(target):

    s="("
    for j in range(weapon):
        if (j==weapon-1):
            r=""
        else:
            r="+"
        s +="x"+str(j+1)+"_"+str(i+1) + r
    s +=")"
    constraints.append(s+"<=0+M*y"+str(i)+";")
    s +="*"
    p="("
    for k in range(target+1):
        if (k==i+1):
            continue
    #    p +="s" +str(k) +str(i+1)+"*h"+str(k) +str(i+1)+"+"
        p += str(setup[k][i+1]) + "*h" + str(k) +"_"+ str(i + 1) + "+"
    p= str(v*1000/3600)+"*"+p.rstrip(p[-1])
    rr=s+str(distances[i]*1000)+"+"+p+")>="+str(minMenzil*1.1)+"-M*(1-y"+str(i)+")"#+"/"+str(v)
    constraints.append(rr+";")
    constraints.append("@bin(y" + str(i) + ");")
cstp="stp="
for i in range (target+1):
    for j in range (target+1):
        if (i==j):
            continue
        cstp += str(setup[i][j])+"*h"+str(i)+"_"+str(j) +"+"

cstp = cstp.rstrip(cstp[-1])
constraints.append("!Toplam Setup süresi;")
constraints.append(cstp+";")
constraints.append("!Grup 5: Bekleme durumundan ilk angajmana geçiş kısıtları ;")

for i in range(target+1):
    cnst=""
    for j in range(target+1):
        if (i==j):
            continue
        cnst +="h"+str(j)+"_"+str(i) +"+"
    cnst = cnst.rstrip(cnst[-1])
    cnst +="=1;"
    constraints.append(cnst)

for j in range(target+1):
    cnst=""
    for i in range(target+1):
        if (i==j):
            continue
        cnst +="h"+str(j)+"_"+str(i) +"+"
    cnst = cnst.rstrip(cnst[-1])
    cnst +="=1;"
    constraints.append(cnst)

constraints.append("!Başlangıçta seçilen hedeften tekrar başlangıç durumuna geçilemez;")

'''
for i in range(target+1):
    cnst=""
    for j in range(target+1):
        if (i==j):
            continue
        cnst +="h"+str(j)+"_"+str(i) +"+"
    cnst = cnst.rstrip(cnst[-1])
    sag=""
    for b in range(weapon):
        sag +="x"+str(b+1)+"_"+str(i)+"+"
    if (i==0):
        sag="1"
        cnst += "=" + sag
    else:
        cnst += "<=" + sag
        l = len(cnst)
        cnst = cnst[:l - 1]

    constraints.append(cnst+";")

for i in range(target+1):
    cnst=""
    for j in range(target+1):
        if (i==j):
            continue
        cnst +="h"+str(j)+"_"+str(i) +"+"
    cnst = cnst.rstrip(cnst[-1])
    cnst+="=1"
    #constraints.append(cnst+";")
'''
#constraints.append("!Başlangıçta seçilen hedeften tekrar başlangıç durumuna geçilemez;")
for i in range(target+1):
    cns=""
    for j in range(i,target+1):
        if (i==j):
            continue
        cns ="h"+str(i)+"_"+str(j) +"+" + "h"+str(j)+"_"+str(i)+"<=1"
        constraints.append(cns+";")

for i in range(weapon+1):
    cns=""
    for j in range(target+1):
        cns = "@bin(x"+str(i+1)+"_"+str(j+1)+")"
        constraints.append(cns+";")

for i in range(target+1):
    for j in range(target+1):
        if (i==j):
            continue
        cns = "@bin(h"+str(i)+"_"+str(j)+")"
        constraints.append(cns+";")


f=open("D:/temp/Problem"+str(target)+"_"+str(weapon)+".txt", "w")
for g in goallist:
    print(g)

for g in goallist:
    f.write(g + "\n")

for i in constraints:
    #f.write(i+"\n")
    print(i)

f.close()

