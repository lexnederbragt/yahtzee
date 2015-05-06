
# coding: utf-8

# **Issues**  
# 
# * 'Two pairs' missing as result
# * 'Full house (2 + 3)' missing as result

# In[ ]:

import itertools
from collections import Counter, namedtuple


# In[ ]:

class score:
    """
    Holds dice frequencies and score results for a throw
    """
    def __init__(self, throw):
        self.throw = throw
        self.frequencies = get_dice_frequencies(throw)
        self.results = get_throw_result(throw, self.frequencies)


# In[ ]:

def get_dice_frequencies(throw):
    """
    Returns a dictionary with the counts of unique dice, pairs, three of a kind etc
    Examples:
    '222333' returns {'Three of a kind': ['2', '3']}
    '123344' returns {'Pair': ['3', '4'], 'Single': ['1', '2']}
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

def dicesum(throw):
    """
    Returns the sum of all dices in a throw
    """
    return sum([int(i) for i in throw])


# In[ ]:

def get_throw_result(throw, dice_frequencies):
    """
    Determines the type of throw:
    Full/Big/Small straight
    Maxi Yahtzee, 5/4/3 equal
    3/2/1 pair(s)
    Tower and Castle
    To Do: number of 1's, 2's, 3's, ... for the top part of the scoring table
    """
    
    # check input
    assert type(throw) is str, 'String expected, but "%r" is %r' % (throw, type(throw))
    assert len(throw) == 6, 'Throw expected to be 6 characters, not %i' % len(throw)
    assert set('123456') == set('123456' + throw), 'Only dices between 1 and 6 allowed, found "%s"' % throw

    # process
    throw_type = ''
    throw_results = []
    if throw == '123456':
        throw_results.append(result('Full straight', '123456', 21))
    if ''.join(sorted(set(throw)))[0:5] == '12345':
        throw_results.append(result('Small straight', '12345', 15))
    if ''.join(sorted(set(throw)))[-5:] == '23456':
        throw_results.append(result('Big straight', '23456', 20))

    # Collect dice frequencies
    # test for pairs, three of a kind, ..., Maxi Yahtzee
    for f in range(2,7):
        result_type = types[f]
        if result_type in dice_frequencies:
            for dice in dice_frequencies[result_type]:
                throw_results.append(result(result_type, dice, f * int(dice)))
    # test for Tower, Castle, Two pairs, Three pairs
    if 'Pair' in dice_frequencies and len(dice_frequencies['Pair']) == 3:
        throw_results.append(result('Three pairs', throw, dicesum(throw)))
    if 'Three of a kind' in dice_frequencies and len(dice_frequencies['Three of a kind']) == 2:
        throw_results.append(result('Castle (3 + 3)', throw, dicesum(throw)))
    if 'Four of a kind' in dice_frequencies and 'Pair' in dice_frequencies:
        throw_results.append(result('Tower (4 + 2)', throw, dicesum(throw)))
    if len(throw_results) < 1 :
        raise Exception("Unknown combination of dice: " , throw)
    return throw_results


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
    assert get_throw_result('111122', get_dice_frequencies('111122')) ==     [result(type='Pair', dice='2', score=4),
     result(type='Four of a kind', dice='1', score=4),
     result(type='Tower (4 + 2)', dice='111122', score=8)]
def test_Three_pairs():
    assert get_throw_result('112244', get_dice_frequencies('112244')) ==     [result(type='Pair', dice='1', score=2),
     result(type='Pair', dice='2', score=4),
     result(type='Pair', dice='4', score=8),
     result(type='Three pairs', dice='112244', score=14)]
def test_Five_of_a_kind():
    assert get_throw_result('444441', get_dice_frequencies('444441')) ==     [result(type='Five of a kind', dice='4', score=20)]
def test_Maxi_yahtzee():
    assert get_throw_result('222222', get_dice_frequencies('222222')) ==     [result(type='Maxi Yahtzee', dice='2', score=12)]


# In[ ]:

def test_dicesum_123456():
    assert dicesum('123456') == 21, dicesum('123456')
def test_dicesum_222222():
    assert dicesum('222222') == 12, dicesum('222222')


# In[ ]:

def test_dice_too_low_high_fail():
    try:
        t = get_throw_result('012345', get_dice_frequencies('012345'))
    except AssertionError, e:
        assert e.message == 'Only dices between 1 and 6 allowed, found "012345"', e.message
def test_dice_as_int_not_string_fail():
    try:
        t = get_throw_result(123456, get_dice_frequencies('123456'))
    except AssertionError, e:
        assert e.message == 'String expected, but "123456" is <type \'int\'>', e.message
def test_dice_too_short_fail():
    try:
        t = get_throw_result('12345', get_dice_frequencies('12345'))
    except AssertionError, e:
        assert e.message == 'Throw expected to be 6 characters, not 5', e.message


# In[ ]:

result = namedtuple('result', ['type', 'dice', 'score'])
types = ',Single,Pair,Three of a kind,Four of a kind,Five of a kind,Maxi Yahtzee'.split(',')


# In[ ]:

if __name__ == '__main__':
    dices = [i for i in range(1, 7)]
    throws = {}
    all_scores = {}
    # the code below is overkill in that it generates all 46656 combinations of 6 dice throws
    # but the resulting unique set is 462 combination, which seems to be correct
    for i in itertools.product(dices, dices, dices, dices, dices, dices):
        throw = ''.join([str(j) for j in sorted(i)])
        throws[throw] = ''
    # adding score to each throw
    for throw in sorted(throws):
        all_scores[throw] = score(throw)
        print throw, [(t.type, t.dice, t.score) for t in all_scores[throw].results]

