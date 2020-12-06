import numpy as np
import matplotlib.pyplot as plt
import time

#question 2
def generateNormalVectors(n, m) :
    """
    :param n: nombre de vecteurs à générer
    :param m: moyenne et écart type de la loi normale
    :return: np array de n vecteurs dont les valeurs sont tirées sur la loi normale de moyenne m et d'écart type m/4
    """
    vec = []
    for i in range(n) :
        vec.append(np.random.normal(m, m/4, 2))
    return np.array(vec)

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

def naiveDominance(s, brk = True): # O(n^2), dumb (remove break for very dumb version)
    """

    :param s: un ensemble de vecteurs à comparer
    :param brk: laissez à True pour arreter d'étudier un point une fois qu'il est dominé, avec brk = False c'est très long
    :return: un ensemble de vecteurs pareto optimaux en minimisation
    """

    result = []
    for d1 in s:
        add = True
        for d2 in s:
            if (d2 <= d1).all() and not (d2 == d1).all():
                add = False
                if brk :
                    break # sans le break, on atteint les tailles 5000 en 10h environ
        else: # else of the for
            if add :
                result.append(d1) # non dominated

    return np.stack(result)

def lessNaiveDominance(s) :
    """
    version raté de la dominance naive
    :param s: un ensemble de vecteurs à comparer
    :return: un ensemble de vecteurs pareto optimaux en minimisation
    """
    domine = []
    for i in range(len(s)) :
        neither = True
        newdomine = []
        for d in range(len(domine)) :
            res = compareMin(s[i], domine[d])
            if not res == "dominates":
                newdomine.append(domine[d])
            if res == "dominated":
                neither = False
        if neither :
            newdomine.append(s[i])
        domine = newdomine
    return np.array(domine)

#question 4
def lexicomp(v, w, ordre = (0, 1)) :
    """
    :param v: vecteur (arraylist)
    :param w: vecteur (arraylist)
    :param ordre: tuple, liste ou vecteur de taille inférieure ou égale à calle de v et w
    :return: comparaison lexicographique de v à w
    """
    for i in ordre :
        if v[i] < w[i] :
            return "inf"
        if v[i] > w[i] :
            return "sup"
    return "equal"


def QuickLexicoSort(l, ordre = (0, 1)) :
    """
    :param l: un array de vecteurs correspondant aux points
    :param ordre: un tuple de taille inférieure ou égale à celle des points
    :return: le tri lexicographique des points selon l'ordre donné
    """
    less = []
    equal = []
    greater = []

    if len(l) > 1:
        pivot = l[0]
        for x in l:
            res = lexicomp(x, pivot, ordre)
            if res == "inf":
                less.append(x)
            elif res == "equal":
                equal.append(x)
            elif res == "sup":
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
    dom = [l[0]]
    for i in l :
        if i[1] < min :
            min = i[1]
            dom.append(i)
    return np.array(dom)

#question5
def test() :
    """
    teste les fonctions de détermination de front de pareto graphiquement
    :return: none
    """
    data = generateNormalVectors(100, 5)

    fig, axs = plt.subplots(1, 3, figsize=(10, 5))
    [ax.plot(*data.T, '+') for ax in axs]

    optimal_lex = lexicoDominance(data)
    optimal_dumb = naiveDominance(data)
    optimal_less_dumb = lessNaiveDominance(data)
    axs[0].plot(*optimal_lex.T, 'o')
    axs[1].plot(*optimal_dumb.T, 'o')
    axs[2].plot(*optimal_less_dumb.T, 'o')


    plt.show()

def question5(brk = True) :
    times_dumb = []
    times_less_dumb = []
    times_lex = []

    nmax = 10000

    if not brk :
        nmax = 2000

    for n in range(200, nmax, 200):
        print(n)
        data = [generateNormalVectors(n, 1000) for _ in range(50)]
        start = time.time()
        for i in range(len(data)):
            optimal = lexicoDominance(data[i])
        times_lex.append((time.time() - start) / 50)

        start = time.time()
        for i in range(len(data)):
            optimal = naiveDominance(data[i], brk = brk)
        times_dumb.append((time.time() - start) / 50)

        start = time.time()
        for i in range(len(data)):
            optimal = lessNaiveDominance(data[i])
        times_less_dumb.append((time.time() - start) / 50)

    fig = plt.figure()
    plt.plot(range(200, nmax, 200), times_lex, label = "lexico")
    plt.plot(range(200, nmax, 200), times_less_dumb, label = "naif amélioré")
    plt.plot(range(200, nmax, 200), times_dumb, label = "naif")
    plt.xlabel("taille de l'ensemble de vecteurs")
    plt.ylabel("temps pour déterminer le front de Pareto (s)")
    plt.legend()
    plt.show()
    fig.savefig("compLexiNaif.png")

#question 7
dynaMOSStab = dict()

def dynaMOSS(k, n, l, clear = False) :
    global dynaMOSStab
    """
    :param k: nombre de vecteurs à choisir
    :param n: nombre de vecteurs disponibles au choix
    :param l: liste des vecteurs
    :return: l'ensemble des images des ensembles de vecteurs de l d'indice inférieur à n de taille k Pareto optimaux (minimisation)
    
    pour trouver le front de pareto, appeler avec k = 1
    """


    if clear :
        dynaMOSStab = dict()

    if (    dynaMOSStab.get((k,n), np.array([-1, -1]) ) != np.array([-1, -1])      ).any() :
        return dynaMOSStab.get((k,n))

    if(k == 0) :
        return np.array([[0, 0]])

    if n-1 < k :
        a = dynaMOSS(k-1, n-1, l) + l[n-1]

        return a
    #print("get : " + str(k) + " in " + str(n))
    a = lexicoDominance( np.concatenate(       (dynaMOSS(k-1, n-1, l) + l[n-1],  dynaMOSS(k, n-1, l)))        )
    dynaMOSStab[(k, n)] = a
    return a


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
def procDeuxTemps(l, k, I) :
    """

    :param l: liste des vecteurs
    :param k: taille de l'ensemble à sélectionner
    :param I: un tuple contenant alphamin et alphamax
    :return: le point minimax des sous ensembles de l
    """

    n = len(l)-1
    pareto = dynaMOSS(k, n, l, clear = True)
    #print(pareto)
    return minimaxEns(pareto, I)


# question 11

def testIdom() :
    data = generateNormalVectors(100, 5)

    """
    fig, axs = plt.subplots(1, 3, figsize=(10, 5))
    [ax.plot(*data.T, '+') for ax in axs]

    optimal_lex = lexicoDominance(data)
    """


    optimal_I = procIdom(data, 10, 0.00001, 0.99999)
    optimal_2T =  procDeuxTemps(data, 10, [0.00001, 0.99999])

    print(optimal_I)
    print(optimal_2T)

    """
    axs[0].plot(*optimal_lex.T, 'o')
    axs[1].plot(*optimal_I.T, 'o')
    axs[2].plot(*optimal_2T.T, 'o') # c'est normal si il y a qu'un seul point, c'est que c'est le minimax   
    plt.show()
    """


def procIdom(points, k, amin, amax) :
    #on prend les points et on les transforme pour la pareto dominance :
    #on a le droit de faire ça
    pointsBis = []
    for p in points :
        pointsBis.append(np.array([p[0]*amin + p[1]*(1-amin), p[0]*amax + p[1]*(1-amax)]))

    #on détermine les points pareto optimaux avec l'approche lexicographique :
    Pareto = dynaMOSS(k, len(points), np.array(pointsBis), clear = True)

    #on transforme le front de pareto pour le mettre dans l'espace voulu
    Idom = []
    for p in Pareto :
        y1 = (p[1] - p[0]*(1-amax)/(1-amin))/amax * amax*(1-amin)/ (amax*(1-amin) + amin * (1- amax))
        y2 = (p[0] - p[1]*amin/amax)/(1-amin) * ((1-amin)*amax/((1-amin)*amax - (1-amax) * amin))
        Idom.append(np.array([y1, y2]))
    #print(Idom)


    return minimaxEns(Idom, [amin, amax])
    return np.array(Idom)


#question 12
# j'ai pas compris à quoi k servait
# TODO : k sert à quoi ?


def question12() :
    times_2T = []
    times_Idom = []
    n = 50
    k= 10
    m = 1000

    for i in np.arange(0.025, 0.525, 0.025) :
        alphamin = 0.5-i
        alphamax = 0.5+i
        print(i)
        data = [generateNormalVectors(n, m) for _ in range(50)]
        start = time.time()
        for i in range(len(data)):
            minimax = procDeuxTemps(data[i], k, [alphamin, alphamax])
        times_2T.append((time.time() - start) / 50)

        start = time.time()
        for i in range(len(data)):
            minimax = procIdom(data[i], k, alphamin, alphamax)
        times_Idom.append((time.time() - start) / 50)

    fig = plt.figure()
    plt.plot( np.arange(0.025, 0.525, 0.025), times_2T, label="méthode en deux temps")
    plt.plot( np.arange(0.025, 0.525, 0.025), times_Idom, label="méthode par I-dominance")
    plt.xlabel("rayon de I centré en 0.5 dans R")
    plt.ylabel("temps pour trouver le point minimax (s)")
    plt.title("comparaison de la méthode en deux temps et de la méthode par I-dominance")
    plt.legend()
    plt.show()
    fig.savefig("compt2T_Idom.png")


#test()

"""
for i in range(50) :
    print("test :")
    testIdom()
    """

#question5()
#question5(brk = False) #décommentez pour utiliser une version naive en O(n^2), attention c'est très très long (plus de 10h)
question12()