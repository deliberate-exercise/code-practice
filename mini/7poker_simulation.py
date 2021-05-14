import random
from collections import defaultdict, Counter

# 7포커 족보 획득 확률 

# 포커 카드 섞기
def shuffler():
    suit = [i for i in range(4)]
    denom = [i for i in range(1, 14)]
    deck = [(s, d) for s in suit for d in denom]
    
    random.shuffle(deck)
    return deck


# 족보 확인
def made(hands):
    arr = [0]
    suit = []
    denom = []
    for h in hands:
        suit.append(h[0])
        denom.append(h[1])
    
    count_denom = Counter(denom).most_common(2)
    if count_denom[0][1] == 2 and count_denom[1][1] == 1: arr.append(1)     # 원 페어
    elif count_denom[0][1] == 2 and count_denom[1][1] == 2: arr.append(2)   # 투 페어
    elif count_denom[0][1] == 3 and count_denom[1][1] != 2: arr.append(3)   # 트리플
    elif count_denom[0][1] == 3 and count_denom[1][1] == 2: arr.append(6)   # 풀 하우스
    elif count_denom[0][1] == 4: arr.append(7)                              # 포 카드


    # 스트레이트 / 플러시 / 스트레이트 플러시 / 로열 스트레이트 플러시
    hand_copy = sorted(hands, key=lambda x: x[1])
    if hand_copy[0][1] == 1: hand_copy.insert(0, (hand_copy[-1][0], 14))

    n_suits = [0]*4
    bin_denom = [[0]*14 for _ in range(5)]
    for s, d in hand_copy:
        if d != 14: n_suits[s] += 1
        bin_denom[s][d-1] = 1
        bin_denom[4][d-1] = 1
    
    for i in range(4):
        flush = False
        straight = False
        royal = False
        if n_suits[i] < 5: continue
        else:
            flush = True
            for j in range(10):
                if sum(bin_denom[i][j:j+5]) == 5: 
                    straight = True
                    if j == 9: royal = True

        if flush and straight and royal: arr.append(9)
        elif flush and straight: arr.append(8)
        elif flush: arr.append(5)

    straight = False
    for j in range(10):
        if sum(bin_denom[4][j:j+5]) == 5: straight = True
                    
    if straight: arr.append(4)
    
    return max(arr)

    
def simulator(n_times):
    arr = [0]*10
    for _ in range(n_times):
        deck = shuffler()
        hand = deck[:7]
        arr[made(hand)] += 1
    
    return arr


# 시뮬레이션 및 결과 출력
n_times = 1000000
simulation = simulator(n_times)
hands = [
    'High Card', 'One Pair', 'Two Pair', 'Triple', 'Straight', 
    'Flush', 'Full House', 'Four Card', 'Straight Flush', 'Royal Straight Flush'
]
probs = map(lambda x: x*100/n_times, simulation)

for h, p in zip(hands, probs): print(h.ljust(30), p)
