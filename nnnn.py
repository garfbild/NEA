import random
import math

def g(x):
    return 1/(math.exp(-1*x)+1)

def gp(x):
    return x*(1-x)

def Matrix(I, J):
    m = []
    for i in range(I):
        m.append([random.uniform(-1,1)]*J)
    return m

def hypothesis(x,a1,a2,a3,InputsWeights,HiddenWeights,InputsNum,HiddenNum,OutputNum):
    for i in range(InputsNum):
        a1[i] = x[i]
    for j in range(HiddenNum):
        Sum = 0
        for i in range(InputsNum):
            Sum += a1[i]*InputsWeights[i][j]
        a2[j] = g(Sum)

    for j in range(OutputNum):
        Sum = 0
        for i in range(HiddenNum):
            Sum += a2[i]*HiddenWeights[i][j]
        a3[j] = g(Sum)
    print(a3)

InputsNum = 2
HiddenNum = 3
OutputNum = 1

a1 = [1.0]*InputsNum
a2 = [1.0]*HiddenNum
a3 = [1.0]*OutputNum

InputsWeights = Matrix(InputsNum,HiddenNum)
HiddenWeights = Matrix(HiddenNum,OutputNum)

for i in range(InputsNum):
    for j in range(HiddenNum):
        InputsWeights[i][j] = random.uniform(-1,1)

for i in range(HiddenNum):
    for j in range(OutputNum):
        HiddenWeights[i][j] = random.uniform(-1,1)

x_data = [[1,1],[0,1],[1,0],[0,0]]
y_data = [0,1,1,0]

for k in range(100000):
    out_d = [0.0]*OutputNum
    hid_d = [0.0]*HiddenNum
    #forward propagate
    for m in range(len(y_data)):
        for i in range(InputsNum):
            a1[i] = x_data[m][i]

        for j in range(HiddenNum):
            Sum = 0
            for i in range(InputsNum):
                Sum += a1[i]*InputsWeights[i][j]
            a2[j] = g(Sum)

        for j in range(OutputNum):
            Sum = 0
            for i in range(HiddenNum):
                Sum += a2[i]*HiddenWeights[i][j]
            a3[j] = g(Sum)
        
        #back propagte the gradients
        for i in range(OutputNum):
            error =  y_data[m] - a3[i]
            out_d[i] = gp(a3[i])*error

        for i in range(HiddenNum):
            error = HiddenWeights[i][0]*out_d[0]
            hid_d[i] = error*gp(a2[i])

        #gradient descent
        for i in range(HiddenNum):
            for j in range(OutputNum):
                a = out_d[j]*a2[i]
                HiddenWeights[i][j] = HiddenWeights[i][j] + 0.5*a

        for i in range(InputsNum):
            for j in range(HiddenNum):
                a = hid_d[j]*a1[i]
                InputsWeights[i][j] = InputsWeights[i][j] + 0.5*a

    if k%10000 == 0:
        error = 0.0
        for m in range(len(y_data)):
            for i in range(InputsNum):
                a1[i] = x_data[m][i]

            for j in range(HiddenNum):
                Sum = 0
                for i in range(InputsNum):
                    Sum += a1[i]*InputsWeights[i][j]
                a2[j] = g(Sum)

            for j in range(OutputNum):
                Sum = 0
                for i in range(HiddenNum):
                    Sum += a2[i]*HiddenWeights[i][j]
                a3[j] = g(Sum)
            error+= y_data[m]*math.log(a3[0]) + (1-y_data[m])* math.log(1-a3[0])
            

        print(error)
for i in range(4):
    hypothesis(x_data[i],a1,a2,a3,InputsWeights,HiddenWeights,InputsNum,HiddenNum,OutputNum)
