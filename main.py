import numpy as np
import matplotlib.pyplot as plt

#question 2
def generateNormalVectors(n, m) :
    """
    :param n: nombre de vecteurs à générer
    :param m: moyenne et écart type de la loi normale
    :return: liste de n vecteurs dont les valeurs sont tirées sur la loi normale de moyenne m et d'écart type m/4
    """
    vec = []
    for i in range(n) :
        vec.append(np.random.normal(m, m/4, 2))
    return vec

#question 3
def compareMin(compared, comparison) :
    """
    :param compared: un vecteur de flottants ou d'entiers ou quoi que ce soit tant qu'il y a un ordre
    :param comparison: un autre vecteur de flottants ou d'entiers ou quoi que ce soit tant qu'il y a un ordre
    :return: comment compared se compare à comparison en minimisation
    """
    dominated = True
    dominates = True
    for i in range(len(compared)) :
        if(compared[i] < comparison[i]) :
            dominated = False
        if(compared[i] > comparison[i]) :
            dominates = False
    if dominated :
        return "dominated"
    elif dominates :
        return "dominates"
    else :
        return "neither"

def naiveDominance(s) :
    """
    :param s: un ensemble de vecteurs à comparer
    :return: un ensemble de vecteurs pareto optimaux en minimisation
    """

    domine = set()
    for i in s :
        neither = True
        for d in domine :
            res = compareMin(i, d)
            if res == "dominates":
                domine.add(i)
                domine.remove(d)
                neither = False
            if res == "dominated":
                neither = False
        if neither :
            domine.add(i)
    return domine

#question 4
def lexicomp(v, w, ordre = (0, 1)) :
    for i in ordre :
        if v[i] < w[i] :
            return "inf"
        if v[i] > w[i] :
            return "sup"
    return "equal"


def QuickLexicoSort(l, ordre = (0, 1)) :
    less = []
    equal = []
    greater = []

    if len(l) > 1:
        pivot = l[0]
        for x in l:
            if lexicomp(x, pivot, ordre) == "inf":
                less.append(x)
            elif lexicomp(x, pivot, ordre) == "equal":
                equal.append(x)
            elif lexicomp(x, pivot, ordre) == "sup":
                greater.append(x)
        return QuickLexicoSort(less) + equal + QuickLexicoSort(greater)
    else:
        return l
    return l

def lexicoDominance(L) :
    """

    :param L: Un array de vecteurs
    :return: le front de pareto de cet ensemble en minimisation
    """
    l = QuickLexicoSort(L)
    #un vecteur n'est pas dominé ssi sa seconde composante est inférieure au minimum des secondes composantes croisées jusque là
    #ne marche de cette manière que pour le bicritère
    min = l[0][1]
    dom = set()
    for i in l :
        if i[1] < min :
            min = i[1]
            dom.add(i)
    return dom

#question 7
def dynaMOSS(k, n, l) :
    if(k == 0) :
        return np.array(np.zeros(2))
    return lexicoDominance( np.unique(np.concatenate( dynaMOSS(k-1, n-1, l) + l[n],  dynaMOSS(k, n-1, l) )))

#question 8
def f(I, y) :
    """

    :param I: les deux valeurs de alpha
    :param y: y
    :return: fI(y)
    """
    return max(y[0]*I[0]+(1-I[0])*y[1], y[0]*I[1]+(1-I[1])*y[1])

def minimaxEns(l, I) :
    """

    :param l: un array de vecteurs
    :param I: les deux valeurs de alpha
    :return: le point minimax de l selon I
    """
    min = f(I,l[0])
    minel = l[0]
    for i in l :
        val = f(I, i)
        if val < min :
            min = val
            minel = i
    return minel


#question 9
def procDeuxTemps(l, k, n, I) :
    pareto = dynaMOSS(k, n, l)
    return minimaxEns(pareto, I)