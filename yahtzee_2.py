
# coding: utf-8

# In[ ]:

import itertools
from collections import Counter, namedtuple


# In[ ]:

def get_dice_frequencies(throw):
    """
    Returns the counts of unique dice, pairs, three of a kind etc
    """
    c = Counter(throw)
    frequencies = {}
    for i in [str(j) for j in range(1, 7)]:
        if i in c:
            result_type = types[c[i]]
            if result_type in frequencies:
                frequencies[result_type].append(i)
            else:
                frequencies[result_type] = [i]
    return frequencies


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
    Full/Big/Small straight
    Maxi Yahtzee, 5/4/3 equal
    3/2/1 pair
    Tower and Castle
    To Do: number of 1's, 2's, 3's, ... for the top part of the scoring table
    """
    
    # check input
    assert type(throw) is str, 'String expected, but "%r" is %r' % (throw, type(throw))
    assert len(throw) == 6, 'Throw expected to be 6 characters, not %i' % len(throw)

    # process
    throw_type = ''
    throw_results = []
#    dice_counts = Counter(throw).values()
    if throw == '123456':
        throw_results.append(result('Full straight', '123456', 21))
    if ''.join(sorted(set(throw)))[0:5] == '12345':
        throw_results.append(result('Small straight', '12345', 15))
    if ''.join(sorted(set(throw)))[-5:] == '23456':
        throw_results.append(result('Big straight', '23456', 20))

    # Collect dice frequencies
    dice_frequencies = get_dice_frequencies(throw)
    # test for pairs, three of a kind, ..., Maxi Yahtzee
    for f in range(2,7):
        result_type = types[f]
        if result_type in dice_frequencies:
            for dice in dice_frequencies[result_type]:
                throw_results.append(result(result_type, dice, f * int(dice)))
    # test for Tower, Castle, Two pair, Three pair
    if 'Pair' in dice_frequencies and len(dice_frequencies['Pair']) == 3:
        throw_results.append(result('Three pair', throw, dicesum(throw)))
    if 'Three of a kind' in dice_frequencies and len(dice_frequencies['Three of a kind']) == 2:
        throw_results.append(result('Castle (3 + 3)', throw, dicesum(throw)))
    if 'Four of a kind' in dice_frequencies and 'Pair' in dice_frequencies:
        throw_results.append(result('Tower (4 + 2)', throw, dicesum(throw)))
    if len(throw_results) < 1 :
        raise Exception("Unknown combination of dice: " , throw)
    return throw_results


# In[ ]:

types = ',Single,Pair,Three of a kind,Four of a kind,Five of a kind,Maxi Yahtzee'.split(',')
dices = [i for i in range(1, 7)]
throws = {}
result = namedtuple('result', ['type', 'dice', 'score'])
# the code below is overkill in that it generates all 46656 combinations of 6 dice throws
# but the resulting unique set is 462 combination, which seems to be correct
for i in itertools.product(dices, dices, dices, dices, dices, dices):
    throw = ''.join([str(j) for j in sorted(i)])
    throws[throw] = ''


# In[ ]:

for throw in sorted(throws):
    throw_results = get_throw_result(throw)
    print throw, [(t.type, t.dice, t.score) for t in throw_results]


# In[ ]:

#get_throw_result('556677')
#Counter('556677')


# In[ ]:

#get_throw_result('1')


# In[ ]:

#get_throw_result(1)


# In[ ]:

def test_dice_frequencies_singles():
    assert get_dice_frequencies('123456') == {'Single': ['1', '2', '3', '4', '5', '6']}
def test_dice_frequencies_3():
    assert get_dice_frequencies('222333') == {'Three of a kind': ['2', '3']}
def test_dice_frequencies_4():
    assert get_dice_frequencies('111122') == {'Four of a kind': ['1'], 'Pair': ['2']}
def test_dice_frequencies_6():
    assert get_dice_frequencies('111111') == {'Maxi Yahtzee': ['1']}


# In[ ]:

def test_Tower():
    assert get_throw_result('111122') == [result(type='Pair', dice='2', score=4),
                                          result(type='Four of a kind', dice='1', score=4),
                                          result(type='Tower (4 + 2)', dice='111122', score=8)]
def test_Three_pairs():
    assert get_throw_result('112244') == [result(type='Pair', dice='1', score=2),
                                          result(type='Pair', dice='2', score=4),
                                          result(type='Pair', dice='4', score=8),
                                          result(type='Three pair', dice='112244', score=14)]

