"""
I write down this code for calculating payoff from put/call option
just for making life eaiser
"""

'''
Input:
    pos: positions, short / long
    S: current price in dollar
    F: future prices
    N: number of assets

Output:
    res: losses / gains from entering the contract
    negative results: losses
    positive results: gains
'''

from turtle import position


def forward_contract(pos, S, F, N):
    if (pos == 'short'):
        return round(N * (F-S),4)
    else:
        return round(N * (S-F),4)


# testcase
## 1.5
print(forward_contract('short', 1.49, 1.5, 100000))
print(forward_contract('short', 1.52, 1.5, 100000))

## 1.6
print(forward_contract('short', 0.513, 0.5, 50000))
print(forward_contract('short', 0.4820, 0.5, 50000))

'''
Input:
    pos: positions, short / long
        - if the pos is "write", that also means short
    type: type of the option, put / call
    S: spot price in dollar
    K: strike price in dollar
    N: number of shares
    costs: the costs of the option

Output:
    res: losses / gains from entering the positions
    negative results: losses
    positive results: gains
'''

def option(pos, type, S, K, N, costs):

    res = N*costs
    if pos == "long":
        # we enter the situation: what is the type of the options?
        res = -res
        if type == 'call':
            if S-K > 0:
                res += (S-K)*N
        elif type == 'put':
            if K-S > 0:
                res += (K-S)*N
        else: # check for invalid input
            print('Invalid input. Try again please.')
    elif pos == 'short' or pos == 'write':
        if type == 'call':
            if S-K > 0:
                res -= (S-K)*N
        elif type == 'put':
            if K-S > 0:
                res -= (K-S)*N
        else: # check for invalid input
            print('Invalid input. Try again please.')
    else: # check for invalid input
        print('Invalid input. Try again please.')

    return res

# testcase
print()
print(option('long','put', 1000, 1200,100, 0.2))
print(option('write','put', 1000, 1200,100, 0.2))

print(option('short','call', 1030, 1200,100, 0.2))
print(option('long','call', 1030, 1200,100, 0.2))



