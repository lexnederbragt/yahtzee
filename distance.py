
# coding: utf-8

# In[ ]:

from yahtzee_2 import get_all_scores, types


# In[ ]:

def get_diff(throw, target):
    """
    Determines the difference between a throw and a target
    E.g. between '111344' and '111144'
    Here, the difference is 1, dice to keep is '11144', to remove is '3'
    """
    diff = 0
    remove = []
    keep = []
    for i, j in zip(throw, target):
        if i != j:
            diff += 1
            remove.append(i)
        else:
            keep.append(i)
    return diff, ''.join(keep), ''.join(remove)


# In[ ]:

# get all throw scores
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

