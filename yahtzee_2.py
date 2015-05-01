
# coding: utf-8

# In[ ]:

import itertools
from collections import Counter, namedtuple


# In[ ]:

dices = [i for i in range(1, 7)]
throws = {}
# the code below is overkill in that it generates all 46656 combinations of 6 dice throws
# but the resulting unique set is 462 combination, which seems to be correct
for i in itertools.product(dices, dices, dices, dices, dices, dices):
    throw = ''.join([str(j) for j in sorted(i)])
    throws[throw] = ''


# In[ ]:

def dice_at_frequency(throw, frequency):
    """
    Determines which dice are at a certain frequency for a throw.
    Examples:
        in throw '112234', '1' and '2' are at frequency 2 (appear 2 times)
        in throw '111134', '1' is at frequency 4 (appears 4 times)
    """
    c = Counter(throw)
    dice_counts = c.values()
    return [int(i) for i in c if c[i] == frequency]


# In[ ]:

def dicesum(throw):
    """
    Returns the sum of all dices in a throw
    """
    return sum([int(i) for i in throw])


# In[ ]:

def get_throw_result(throw):
    """
    Determines the type of throw:
    Full/Big/Smal straight
    Maxi Yahtzee, 5/4/3 equal
    3/2/1 pair
    Tower and Castle
    To Do: number of 1's, 2's, 3's, ... for the top part of the scoring table
    """
    # note that the order of the checks is important!
    
    # check input
    assert type(throw) is str, 'String expected, but "%r" is %r' % (throw, type(throw))
    assert len(throw) == 6, 'Throw expected to be 6 characters, not %i' % len(throw)

    # process
    throw_type = ''
    result = namedtuple('result', ['type', 'score'])
    dice_counts = Counter(throw).values()
    if throw == '123456':
        return result('Full straight', 21)
    elif ''.join(sorted(set(throw))) == '12345':
        return result('Small straight', 15)
    elif ''.join(sorted(set(throw))) == '23456':
        return result('Big straight', 20)
    elif 6 in dice_counts:
        return result('Maxi Yahtzee', 100)
    elif 5 in dice_counts:
        five = dice_at_frequency(throw, 5)[0]
        return result('Five equal', 5 * five)
    elif 4 in dice_counts and 2 in dice_counts:
        return result('Tower (4 + 2)', dicesum(throw))
    elif 4 in dice_counts:
        four = dice_at_frequency(throw, 4)[0]
        return result('Four equal', 4 * four)
    elif dice_counts == [3, 3]:
        return result('Castle (3 + 3)', dicesum(throw))
    elif 3 in dice_counts:
        three = dice_at_frequency(throw, 3)
        return result('Three equal', [3 * i for i in three])
    elif dice_counts == [2, 2, 2]:
        return result('Three pairs', dicesum(throw))
    elif sorted(dice_counts)[-2:] == [2, 2]:
        two = dice_at_frequency(throw, 2)
        return result('Two pairs', sum([2 * i for i in two]))
    elif sorted(dice_counts)[-1:] == [2]:
        two = dice_at_frequency(throw, 2)
        return result('One pair', [2 * i for i in two])
    else:
        raise Exception("Unknown combination of dice: " , throw)
    return throw_type


# In[ ]:

for throw in sorted(throws):
    throw_result = get_throw_result(throw)
    print throw, throw_result.type, throw_result.score
    #if throw_type: print throw, throw_type


# In[ ]:

#get_throw_result('1')


# In[ ]:

#get_throw_result(1)


# In[ ]:

def test_Tower():
    result = get_throw_result('222233')
    assert result.type  == 'Tower (4 + 2)', result.type
    assert result.score == 14, result.score

def test_Three_pairs():
    result = get_throw_result('112244')
    assert result.type  == 'Three pairs', result.type
    assert result.score == 14, result.score


# In[ ]:

two = dice_at_frequency('112234',2)
print two
#[3 * i for i in three]


# In[ ]:



