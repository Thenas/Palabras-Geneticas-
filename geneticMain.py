from random import randint as rand 
from os import system as sys 

POP = 500 # poblacion por generacion 
WORD = "esternocleidomastoideo"  # objetivo al que se desea llegar
RUN = True


def mapping(valor, x1 , y1, x2, y2):
    return ((valor - x1)*(y2-x2) /(y1-x1)) + x2

def crossOver(word1, word2):
    childWord = ""
    tam = len(word1)
    midpoint = rand(0,tam)

    for i in range(midpoint): childWord+=word1[i]
    for i in range(midpoint,tam): childWord += word2[i]
    return childWord

def calcFitness(listString,target):
    temporalFit = 0
    fit = []
    for word in listString:
        for letterW,letter in zip(target,word):
            if letterW == letter: temporalFit += 1
        fit.append(temporalFit)
        temporalFit = 0
    
    fit = list(i/len(target) for i in fit)
    return fit

def generate(popLen,target):
    temporalString = ""
    words = []
    for i in range(popLen):
        for j in range(len(target)): temporalString+=chr(rand(97,122))
        words.append(temporalString)
        temporalString = ""
    return words

class poblacion:
    def __init__(self, target = WORD):
        self.words = generate(POP,target)
        self.target = target
        self.fitness = calcFitness(self.words, self.target)
        self.wordsObj = list(zip(self.words,self.fitness))
        self.maxFitness = 0
        self.lovePool  =[]
 
    
    def naturalSelection(self):
        self.lovePool = []
        self.maxFitness = max(self.fitness)
        if self.maxFitness == 0: self.lovePool = self.words
        else:
            for word,fit in self.wordsObj:
                for i in range(int(fit*100)): self.lovePool.append(word)

    def selfGenerate(self):
        self.words = []
        for i in range(POP):
            self.words.append(crossOver( self.lovePool[rand(0,len(self.lovePool) - 1)]  ,  self.lovePool[rand(0,len(self.lovePool) - 1)] ))
        self.fitness = calcFitness(self.words, self.target)
        self.wordsObj = list(zip(self.words,self.fitness))
            


    def mutate(self,mutaRate):
        if type(mutaRate) is float and mutaRate<1: mutaRate = mutaRate*100 
        temporalwords = []  
        for word in self.words:
            for i in range(len(word)):
                if rand(0,100) < int(mutaRate):
                    word = word.replace(word[i], chr(rand(97,122)))
            temporalwords.append(word)
        self.words = temporalwords
        self.fitness = calcFitness(self.words,self.target)
         

popu = poblacion()
generacion1 = popu.words

gene = 0
localMaxFitness = 0
moreFitWord = ""
while RUN:
    sys('cls')
    maxWordObj =  max(popu.wordsObj)
    print("Mas apto generacion: " + str(maxWordObj[0])   +   "      Fitness: " +  str(maxWordObj[1])  + "       Generacion: " + str(gene) +  "     el mas apto: " + str(moreFitWord) + "      fitness: "  +str(localMaxFitness) )
    if( maxWordObj[1]  > localMaxFitness):
        localMaxFitness = maxWordObj[1]
        moreFitWord = maxWordObj[0]
    
    popu.naturalSelection()    
    popu.selfGenerate()
    popu.mutate(100)
    

    if maxWordObj[1] == 1: 
        RUN = False 
        sys('cls')
        print("Resultado : " + str(maxWordObj[0])    +   "      Fitness: " +  str(maxWordObj[1]) , "           generacion final: " , str(gene) )
    gene +=1