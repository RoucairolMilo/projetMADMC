import numpy as np
import matplotlib.pyplot as plt

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

def lexicoDominance(s) :
    l = QuickLexicoSort(list(s))
    #un vecteur n'est pas dominé ssi sa seconde composante est inférieure au minimum des secondes composantes croisées jusque là
    #ne marche de cette manière que pour le bicritère
    min = l[0][1]
    dom = []
    for i in l :
        if i[1] < min :
            min = i[1]
            dom.append(i)
    return dom


l = generateNormalVectors(10, 1)

print(l)

print(QuickLexicoSort(l))
