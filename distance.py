
# coding: utf-8

# In[ ]:

from yahtzee_2 import get_all_scores, types


# In[ ]:

type_descriptions = {'Tower (4 + 2)' : ['Pair', 'Four of a kind']}
description_counts = {}
for i,j in enumerate(types):
    description_counts[j] = i


# In[ ]:

def get_diff(throw_in, target):
    diff = 0
    remove = []
    keep = []
    for i, j in zip(throw_in, target):
        if i != j:
            diff += 1
            remove.append(i)
        else:
            keep.append(i)
    return diff, ''.join(keep), ''.join(remove)


# In[ ]:

all_scores = get_all_scores()


# In[ ]:

throw_in = '111344'
desired_type = 'Castle (3 + 3)' #'Maxi Yahtzee' # 'Tower (4 + 2)':
shortest_dist = {6: None}
for throw in all_scores:
    for result in all_scores[throw].results:
        if result.type == desired_type:
            (dist, keep, remove) = get_diff(throw_in, throw)
            print throw, "distance %r, keep %r, remove %r" % (dist, keep, remove)
            if dist < shortest_dist.keys()[0]:
                shortest_dist= {dist : (throw, keep, remove)}
print shortest_dist


# In[ ]:

# from http://stackoverflow.com/questions/2460177/edit-distance-in-python
#this calculates edit distance not levenstein edit distance
def distance(word1, word2):
    len_1=len(word1)
    len_2=len(word2)

    x =[[0]*(len_2+1) for _ in range(len_1+1)]#the matrix whose last element ->edit distance

    for i in range(0,len_1+1): #initialization of base case values
        x[i][0]=i
    for j in range(0,len_2+1):
        x[0][j]=j
    for i in range (1,len_1+1):
        for j in range(1,len_2+1):
            if word1[i-1]==word2[j-1]:
                x[i][j] = x[i-1][j-1] 
            else :
                x[i][j]= min(x[i][j-1],x[i-1][j],x[i-1][j-1])+1
    return x[i][j]


# In[ ]:

word1="rosettacode"
word2="raisethysword"
distance('112233', '11223')


# In[ ]:



