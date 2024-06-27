import random
import copy


def partition(n, m, minQuota, maxQuota):
    quotas = []

    while len(quotas) < m:
        x = random.randint(minQuota, maxQuota)
        quotas.append(x)

    random.shuffle(quotas)

    if sum(quotas) > n:

        lt = copy.deepcopy([x for x in quotas if x == minQuota])
        gt = copy.deepcopy([x for x in quotas if x > minQuota])

        temp = list()
        req = sum(quotas) - n

        while req > 0:
            x = random.choice(gt)
            gt.remove(x)
            x -= 1
            req -= 1
            if x == minQuota:
                temp.append(x)
            else:
                gt.append(x)

        result = gt + temp + lt


    elif sum(quotas) < n:

        req = n - sum(quotas)

        lt2 = copy.deepcopy([x for x in quotas if x < maxQuota])
        gt2 = copy.deepcopy([x for x in quotas if x == maxQuota])

        temp = list()

        while req > 0:

            x = random.choice(lt2)
            lt2.remove(x)
            x += 1
            req -= 1
            if x == maxQuota:
                temp.append(x)
            else:
                lt2.append(x)

        result = gt2 + temp + lt2

    else:

        result = quotas

    return result
