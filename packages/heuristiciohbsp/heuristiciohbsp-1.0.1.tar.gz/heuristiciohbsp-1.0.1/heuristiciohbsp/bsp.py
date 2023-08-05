import quick_ioh as qioh

def ioh(L,n,l,d,smallitem = 0):
    #Initial Parameters
    n=len(d)
    soma = leftover = loss = 0
    bar = 1
    smallitem = smallitem
    x_ret = []

    #Sorting
    qioh.quickSort(l,d,0,n-1)

    #Put together items of the same size
    i=0
    while i<(n-1):
        if l[i]==l[i+1]:
            d[i]=d[i]+d[i+1]
            l.pop(i+1)
            d.pop(i+1)
            n=n-1
        else:
            i=i+1
        if i==n:
            break
    n=len(d)
    
    #SUM OF DEMAND ITEMS
    for i in range(n):
        soma = soma + d[i]
    
    #small item
    if smallitem == 0:
        small_ = l[n-1]
    else:
        small_ = smallitem

    print("small_",small_)
    #Begin
    while (soma > 0):
        L_hat = L
        x = [0]*n 
        #First branch (IOH)
        for i in range(n):
            if L_hat>=l[i]:
                y = int(L_hat/l[i])
                if(y > d[i]):
                    y = d[i]
        
                x[i] = y
                d[i] -= x[i]
                soma -= x[i]
                L_hat -= (x[i] * l[i])
        
        if L_hat>0:
            find = ideal = 0
            for i in range(1,n,1):
                if ideal==1:
                    break
                if x[i]>0:
                    L_hat_temp=L_hat+(l[i])
                    L_hat_ant=L_hat
                    for j in range(i+1,n,1):
                        if (d[j]-x[j]<=0):
                                break
                        if ideal==1:
                            break
                        selec=l[j]
                        for k in range(n-1,j+1,-1):
                            if ideal==1 or l[j]+l[k]>L_hat_temp:
                                break
                            if d[k]>x[k]:
                                if L_hat_temp-(selec+l[k])>=0 and L_hat_temp-(selec+l[k])<L_hat_ant:
                                    r=[0]*3
                                    r[0]=i
                                    r[1]=j
                                    r[2]=k
                                    L_hat_ant=L_hat_temp-(selec+l[k])
                                    find=1
                                    if L_hat_temp-(selec+l[k])==0:
                                        ideal=1
            if ideal==1 or find==1:
                x[r[0]]-=1
                d[r[0]]+=1
                x[r[1]]+=1
                d[r[1]]-=1
                x[r[2]]+=1
                d[r[2]]-=1
                L_hat=L_hat_ant
                soma +=1
                soma -=2 
                    
            aux=0
            x_ret.append(x)
            for i in range(n):
                if x[i]>0:
                    aux+=l[i]*x[i]
            L_hat=L-aux
        #Remove null demands
        i = 0
        while i <= (n-1):
            if(d[i] == 0):
                l.pop(i)
                d.pop(i)
                n = n-1
            else:
                i=i+1
            if i==n:
                break
        n = len(d) 
        #Add Loss, Leftover and Bar
        if(L_hat < small_):
            loss += L_hat
            L_hat = L
            bar += 1
        else:
            leftover += L_hat
            L_hat = L
            bar += 1
    return(leftover, loss, bar, x_ret)