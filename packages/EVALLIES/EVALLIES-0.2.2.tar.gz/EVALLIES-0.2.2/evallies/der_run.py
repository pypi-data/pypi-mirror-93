# -* coding: utf-8 -*-

#################################################################################
# This file is part of EVALLIES.                                                #
#                                                                               #
# EVALLIES is a python package for lifelong learning speaker diarization.       #
# Home page: https://git-lium.univ-lemans.fr/Larcher/evallies                   #
#                                                                               #
# EVALLIES is free software: you can redistribute it and/or modify              #
# it under the terms of the GNU LLesser General Public License as               #
# published by the Free Software Foundation, either version 3 of the License,   #
# or (at your option) any later version.                                        #
#                                                                               #
# EVALLIES is distributed in the hope that it will be useful,                   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 #
# GNU Lesser General Public License for more details.                           #
#                                                                               #
# You should have received a copy of the GNU Lesser General Public License      #
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.              #
#                                                                               #
#################################################################################
"""
Copyright 2020-2021 Anthony Larcher & Olivier Galibert

    :mod:`der_run`

"""

import numpy as np
from scipy.optimize import linear_sum_assignment
import io
from collections import namedtuple
import sys
import os
import os.path


def make_spkmap(spk):
    spkmap = {}
    spkcount = 0
    spkunmap = []
    for s in spk.speaker:
        if not s in spkmap:
            spkunmap.append(s)
            spkmap[s] = spkcount
            spkcount += 1
    return spkmap, spkunmap, spkcount


def range_to_frontiers(rng):
    rng.sort()
    pos = 0
    while pos < len(rng) - 1:
        if rng[pos][1] >= rng[pos + 1][0]:
            rng[pos] = (rng[pos][0], max(rng[pos][1], rng[pos + 1][1]))
            rng.pop(pos + 1)
        else:
            pos = pos + 1
    front = []
    for r in rng:
        front.append(("n", r[0]))
        front.append(("p", r[1]))
    return front

def filter_frontier_on_uem(front, uem):
    uemi = 0
    fri = 0
    fo = []
    while uemi != len(uem.start_time) and fri != len(front):
        if uem.start_time[uemi] < front[fri][1]:
            if uem.end_time[uemi] >= front[fri][1]:
                if front[fri][0] != 'n':
                    if len(fo) == 0 or fo[-1][1] < uem.start_time[uemi]:
                        fo.append(('n', uem.start_time[uemi]))
                    fo.append((front[fri][0], front[fri][1]))
                else:
                    fo.append((front[fri][0], front[fri][1]))
                fri += 1
            else:
                if front[fri][0] != 'n':
                    if len(fo) == 0 or fo[-1][1] < uem.start_time[uemi]:
                        fo.append(('n', uem.start_time[uemi]))
                    fo.append((front[fri][0], uem.end_time[uemi]))
                uemi += 1
        else:
            fri += 1
    return fo

def filter_frontiers_on_uem(front, uem):
    fo = []
    for fr in front:
        fo.append(filter_frontier_on_uem(fr, uem))
    return fo

def merge_two_frontiers(front1, front2, end1, end2):
    frontr = []
    pos1 = 0
    pos2 = 0
    while pos1 < len(front1) or pos2 < len(front2):
        ctime = (
            front1[pos1][1]
            if pos2 == len(front2)
            else front2[pos2][1]
            if pos1 == len(front1)
            else min(front1[pos1][1], front2[pos2][1])
        )
        mode1 = end1 if pos1 == len(front1) else front1[pos1][0]
        mode2 = end2 if pos2 == len(front2) else front2[pos2][0]
        frontr.append((mode1 + mode2, ctime))
        if pos1 != len(front1) and front1[pos1][1] == ctime:
            pos1 += 1
        if pos2 != len(front2) and front2[pos2][1] == ctime:
            pos2 += 1
    return frontr


def make_merge_frontier(hyp_union, ref_union, ref_frontiers_collar):
    hr = merge_two_frontiers(hyp_union, ref_union, "n", "n")
    frontr = []
    for f in ref_frontiers_collar:
        frontr.append(merge_two_frontiers(hr, f, "nn", "n"))
    return frontr


def make_frontiers(spk, spkmap, spkcount):
    rngs = [[] for i in range(spkcount)]
    for i in range(0, len(spk.speaker)):
        spki = spkmap[spk.speaker[i]]
        rngs[spki].append((spk.start_time[i], spk.end_time[i]))
    front = []
    for r in rngs:
        front.append(range_to_frontiers(r))
    return front


def make_union_frontiers(spk):
    rngs = []
    for i in range(0, len(spk.speaker)):
        rngs.append((spk.start_time[i], spk.end_time[i]))
    return range_to_frontiers(rngs)


def frontiers_add_collar(front, collar):
    cfront = []
    for f in front:
        a = f[1] - collar
        b = f[1] + collar
        if a < 0:
            a = 0
        if len(cfront) == 0 or a > cfront[-1][1]:
            cfront.append((f[0], a))
            cfront.append(("t", b))
        else:
            cfront[-1] = ("t", b)
    return cfront


def make_times(front):
    times = []
    for s in front:
        time = 0
        ptime = 0
        for p in s:
            if p[0] == "n":
                ptime = p[1]
            elif p[0] == "p":
                time += p[1] - ptime
        times.append(time)
    return times


def add_time(thyp, thyn, mode, eh, er, tc, efa, emiss, econf):
    if mode == "ppp":
        return eh, er + thyn, tc + thyp, efa, emiss, econf + thyn
    if mode == "ppn":
        return eh + thyp, er, tc, efa, emiss, econf
    if mode == "ppt":
        return eh, er, tc + thyp, efa, emiss, econf
    if mode == "pnn":
        return eh + thyp, er, tc, efa + thyp, emiss, econf
    if mode == "pnt":
        return eh, er, tc + thyp, efa, emiss, econf
    if mode == "npp":
        return eh, er + thyn, tc, efa, emiss + thyn, econf
    # npn npt nnn nnt
    return eh, er, tc, efa, emiss, econf


def compute_times(frontr, fronth):
    eh = 0
    er = 0
    rc = 0
    efa = 0
    emiss = 0
    econf = 0
    hpos = 0
    tbeg = 0
    thyp = 0
    hypbef = 0
    for f in frontr:
        tend = f[1]
        while hpos < len(fronth):
            dinter = min(fronth[hpos][1], tend)
            if fronth[hpos][0] == "p":
                thyp += dinter - hypbef
            if fronth[hpos][1] > tend:
                break
            hypbef = dinter
            hpos += 1
        eh, er, rc, efa, emiss, econf = add_time(
            thyp, tend - tbeg - thyp, f[0], eh, er, rc, efa, emiss, econf
        )

        if hpos < len(fronth):
            hypbef = min(fronth[hpos][1], tend)
        tbeg = tend
        thyp = 0
    while hpos < len(fronth):
        if fronth[hpos][0] == "p":
            thyp += fronth[hpos][1] - tbeg
        tbeg = fronth[hpos][1]
        hpos += 1
    eh, er, rc, efa, emiss, econf = add_time(
        thyp, 0, "pnn", eh, er, rc, efa, emiss, econf
    )
    return (
        round(eh, 3),
        round(er, 3),
        round(rc, 3),
        round(efa, 3),
        round(emiss, 3),
        round(econf, 3),
    )


def compute_miss(funion, front):
    miss = []
    for f1 in front:
        hpos = 0
        tbeg = 0
        thyp = 0
        hypbef = 0
        fa = 0
        for f in funion:
            tend = f[1]
            while hpos < len(f1):
                dinter = min(f1[hpos][1], tend)
                if f1[hpos][0] == "p":
                    thyp += dinter - hypbef
                if f1[hpos][1] > tend:
                    break
                hypbef = dinter
                hpos += 1
            if f[0] == "n":
                fa += thyp
            if hpos < len(f1):
                hypbef = min(f1[hpos][1], tend)
            tbeg = tend
            thyp = 0
        while hpos < len(f1):
            if f1[hpos][0] == "p":
                thyp += f1[hpos][1] - tbeg
            tbeg = f1[hpos][1]
            hpos += 1
        fa += thyp
        fa = round(fa, 3)
        miss.append(fa)
    return miss


def accumulate_confusion(fref, fhyp, map_rh, map_hr):
    ref_spkcount = len(fref)
    hyp_spkcount = len(fhyp)
    correct_ref = [0] * ref_spkcount
    correct_hyp = [0] * hyp_spkcount
    lost_ref = [0] * ref_spkcount
    lost_hyp = [0] * hyp_spkcount
    confusion_matrix = np.zeros((ref_spkcount, hyp_spkcount), dtype="float64")
    fri = [0] * ref_spkcount
    fhi = [0] * hyp_spkcount
    cur_time = 0
    while True:
        ridx = []
        r_is_t = []
        hidx = []
        time = -1

        # Build the list of who is in the segment
        for i in range(ref_spkcount):
            if fri[i] != len(fref[i]):
                cf = fref[i][fri[i]]
                if time == -1 or cf[1] < time:
                    time = cf[1]
                if cf[0] != "n":
                    ridx.append(i)
                    r_is_t.append(cf[0] == "t")

        for i in range(hyp_spkcount):
            if fhi[i] != len(fhyp[i]):
                cf = fhyp[i][fhi[i]]
                if time == -1 or cf[1] < time:
                    time = cf[1]
                if cf[0] != "n":
                    hidx.append(i)

        if time == -1:
            break

        # Only do the computations when there's something to do
        if len(ridx) > 0 or len(hidx) > 0:
            duration = time - cur_time

            # Hyp and ref mapped together end up in correct time and are removed from the lists
            i = 0
            while i != len(ridx):
                r = ridx[i]
                h = map_rh[r]
                dropped = False
                if h != -1:
                    slot = -1
                    for j in range(len(hidx)):
                        if hidx[j] == h:
                            slot = j
                            break
                    if slot != -1:
                        correct_ref[r] += duration
                        correct_hyp[h] += duration
                        ridx.pop(i)
                        r_is_t.pop(i)
                        hidx.pop(slot)
                        dropped = True
                if not dropped:
                    i += 1

            # Ref in transition is removed from the list if mapped to some hyp
            i = 0
            while i != len(ridx):
                r = ridx[i]
                if r_is_t[i] and map_rh[r] != -1:
                    ridx.pop(i)
                    r_is_t.pop(i)
                else:
                    i += 1

            if len(hidx) == 0:
                # If there's no hyp, we're all in lost_ref
                for r in ridx:
                    lost_ref[r] += duration

            elif len(ridx) == 0:
                # If there's no ref, we're all in lost_hyp
                for h in hidx:
                    lost_hyp[h] += duration

            else:
                # Otherwise we're in confusion.  Amount of confusion time to give
                # is equal to the max of the ref and hyp times
                conf_time = max(len(ridx), len(hidx)) * duration

                # Number of slots, otoh, is equal to the product of the number of
                # refs and hyps
                conf_slots = len(ridx) * len(hidx)

                # Give the time equally in all slots
                conf_one_time = conf_time / conf_slots
                for r in ridx:
                    for h in hidx:
                        confusion_matrix[r, h] += conf_one_time

        # Step all the done segments
        for r in range(ref_spkcount):
            if fri[r] != len(fref[r]) and fref[r][fri[r]][1] == time:
                fri[r] += 1
        for h in range(hyp_spkcount):
            if fhi[h] != len(fhyp[h]) and fhyp[h][fhi[h]][1] == time:
                fhi[h] += 1
        cur_time = time

    return correct_ref, correct_hyp, lost_ref, lost_hyp, confusion_matrix


def compute_der(ref, hyp, uem, map, collar):
    ref_spkmap, ref_spkunmap, ref_spkcount = make_spkmap(ref)
    hyp_spkmap, hyp_spkunmap, hyp_spkcount = make_spkmap(hyp)

    ref_frontiers = filter_frontiers_on_uem(make_frontiers(ref, ref_spkmap, ref_spkcount), uem)
    hyp_frontiers = filter_frontiers_on_uem(make_frontiers(hyp, hyp_spkmap, hyp_spkcount), uem)
    ref_frontiers_collar = []
    for front in ref_frontiers:
        ref_frontiers_collar.append(filter_frontier_on_uem(frontiers_add_collar(front, collar), uem))

    ref_union = filter_frontier_on_uem(make_union_frontiers(ref), uem)
    hyp_union = filter_frontier_on_uem(make_union_frontiers(hyp), uem)

    merge_frontiers = make_merge_frontier(hyp_union, ref_union, ref_frontiers_collar)

    ref_times = make_times(ref_frontiers)
    hyp_times = make_times(hyp_frontiers)

    eh = np.zeros((ref_spkcount, hyp_spkcount), dtype="float64")
    er = np.zeros((ref_spkcount, hyp_spkcount), dtype="float64")
    tc = np.zeros((ref_spkcount, hyp_spkcount), dtype="float64")
    efa = np.zeros((ref_spkcount, hyp_spkcount), dtype="float64")
    emiss = np.zeros((ref_spkcount, hyp_spkcount), dtype="float64")
    econf = np.zeros((ref_spkcount, hyp_spkcount), dtype="float64")
    de = np.zeros((ref_spkcount, hyp_spkcount), dtype="float64")

    miss_hyp = compute_miss(ref_union, hyp_frontiers)
    miss_ref = compute_miss(hyp_union, ref_frontiers)
    
    for r in range(ref_spkcount):
        for h in range(hyp_spkcount):
            (
                eh[r, h],
                er[r, h],
                tc[r, h],
                efa[r, h],
                emiss[r, h],
                econf[r, h],
            ) = compute_times(merge_frontiers[r], hyp_frontiers[h])
            de[r, h] = ref_times[r] + miss_hyp[h] - efa[r, h] - emiss[r, h] - econf[r, h]

    newspkmap = {}
    map_rh = [-1] * ref_spkcount
    map_hr = [-1] * hyp_spkcount
    solved_ref = [0] * ref_spkcount
    solved_hyp = [0] * hyp_spkcount
    for rs in map:
        hs = map[rs]
        newspkmap[rs] = hs
        rid = ref_spkmap[rs] if rs in ref_spkmap else -1
        hid = hyp_spkmap[hs] if hs in hyp_spkmap else -1
        if rid != -1:
            solved_ref[rid] = -1
        if hid != -1:
            solved_hyp[hid] = -1
        if rid != -1 and hid != -1:
            map_rh[rid] = hid
            map_hr[hid] = rid

    solved_ref_back = []
    solved_hyp_back = []
    for i in range(0, ref_spkcount):
        if solved_ref[i] == 0:
            solved_ref[i] = len(solved_ref_back)
            solved_ref_back.append(i)
    for i in range(0, hyp_spkcount):
        if solved_hyp[i] == 0:
            solved_hyp[i] = len(solved_hyp_back)
            solved_hyp_back.append(i)

    solved_ref_count = len(solved_ref_back)
    solved_hyp_count = len(solved_hyp_back)
    opt_size = max(solved_ref_count, solved_hyp_count)
    costs = np.zeros((opt_size, opt_size), dtype="float64")
    for r1 in range(solved_ref_count):
        r = solved_ref_back[r1]
        for h1 in range(solved_hyp_count):
            h = solved_hyp_back[h1]
            costs[r1, h1] = -round(de[r, h] * 1000)            
        
    (map1, map2) = linear_sum_assignment(costs)
    for i1 in range(0, opt_size):
        i = map1[i1]
        j = map2[i1]
        if (
            i < solved_ref_count
            and j < solved_hyp_count
            and de[i, j] > 0
            and tc[i, j] > 0
        ):
            r = solved_ref_back[i]
            h = solved_hyp_back[j]
            map_rh[r] = h
            map_hr[h] = r

    for i, j in enumerate(map_rh):
        if j != -1:
            newspkmap[ref_spkunmap[i]] = hyp_spkunmap[j]

    ref_mixed_frontiers = []
    for r in range(ref_spkcount):
        if map_rh[r] == -1:
            ref_mixed_frontiers.append(ref_frontiers[r])
        else:
            ref_mixed_frontiers.append(ref_frontiers_collar[r])

    (
        correct_ref,
        correct_hyp,
        lost_ref,
        lost_hyp,
        confusion_matrix,
    ) = accumulate_confusion(ref_mixed_frontiers, hyp_frontiers, map_rh, map_hr)

    conf = 0
    for r in range(ref_spkcount):
        for h in range(hyp_spkcount):
            conf += confusion_matrix[r, h]
    totaltime = 0
    miss = 0
    for r in range(ref_spkcount):
        totaltime += ref_times[r]
        miss += lost_ref[r]
    fa = 0
    for h in range(hyp_spkcount):
        fa += lost_hyp[h]

    return 100 * (fa + miss + conf) / totaltime, totaltime, newspkmap

Spki = namedtuple('Spki', ['speaker', 'start_time', 'end_time'])
Uemi = namedtuple('Uemi', ['start_time', 'end_time'])

def load_mdtm(file):
    global Spki
    res = Spki(speaker=[], start_time=[], end_time=[])
    for l in io.open(file):
        e = l.split()
        res.start_time.append(round(float(e[2]), 3))
        res.end_time.append(round(float(e[2]) + float(e[3]), 3))
        res.speaker.append(e[7])
    return res

def load_uem(file):
    global Uemi
    res = Uemi(start_time=[], end_time=[])
    for l in io.open(file):
        e = l.split()
        res.start_time.append(round(float(e[2]), 3))
        res.end_time.append(round(float(e[3]), 3))
    return res

    
def load_map(file):
    res = {}
    for l in io.open(file):
        e = l.split()
        res[e[0]] = e[1]
    return res

def find_file(pdir, names, ext):
    for i in range(0, 2):
        p = pdir + '/' + names[i] + ext
        if os.path.isfile(p):
            return p
    err = ""
    for i in range(0, 2):
        if i == 0:
            err += "Neither "
        else:
            err += " nor "
        err += pdir + '/' + names[i] + ext
    err += ' war found.'
    print(err, file = sys.stderr)
    sys.exit(1)



def der_incremental(lifelong_list, ref_mdtm_dir, ref_uem_dir, hyp_mdtm_dir):

    map = {}

    total_error = 0
    total_time = 0

    for l in open(lifelong_list):
        e = l.split()
        ref = load_mdtm(find_file(ref_mdtm_dir, e, ".mdtm"))
        uem = load_uem (find_file(ref_uem_dir, e, ".uem"))
        hyp = load_mdtm(find_file(hyp_mdtm_dir, e, ".mdtm"))
        (der, time, map) = compute_der(ref, hyp, uem, map, 0.250)
        total_error += der * time
        total_time += time
        #print("%s: DER: %6.2f%%  Time: %.2fs" % (e[0], der, time))

    print("*** Cross Show Incremental DER: %6.2f%%  Total time: %.2fs" % (total_error / total_time, total_time))

    #mapf = open(sys.argv[5], 'w')
    #for s in map:
    #    print("%s %s" % (s, map[s]), file=mapf)


