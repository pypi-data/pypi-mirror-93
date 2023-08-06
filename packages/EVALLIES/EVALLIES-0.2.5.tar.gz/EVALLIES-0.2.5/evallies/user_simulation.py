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

    :mod:`user_simulation`

"""
import numpy as np
import s4d

from scipy.optimize import linear_sum_assignment


def make_spkmap(spk):
    spkmap = {}
    spkcount = 0
    for s in spk.speaker:
        if not s in spkmap:
            spkmap[s] = spkcount
            spkcount += 1
    return spkmap, spkcount


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


def find_common_point(f1, f2):
    fr = merge_two_frontiers(f1, f2, "nn", "n")
    st = None
    en = None
    dur = None
    for i in range(1, len(fr)):
        if fr[i][0] == "pp":
            st1 = fr[i - 1][1]
            en1 = fr[i][1]
            dur1 = en1 - st1
            if dur == None or dur < dur1:
                st = st1
                en = en1
                dur = dur1
    # Should we randomize?  Let's be nice for now
    return (st + en) / 2


def find_best_information(ref, hyp, collar, correction_type=(True, True, True)):
    """

    :param ref:
    :param hyp:
    :param collar:
    :param correction_type: a triplet of boolean. Each value is associated to a type of correction:
        first one is merge two segments, second one: split two segments and third one: modify the frontiers of a segment
    :return:
    """
    ref_spkmap, ref_spkcount = make_spkmap(ref)
    hyp_spkmap, hyp_spkcount = make_spkmap(hyp)

    ref_frontiers = make_frontiers(ref, ref_spkmap, ref_spkcount)
    hyp_frontiers = make_frontiers(hyp, hyp_spkmap, hyp_spkcount)
    ref_frontiers_collar = []
    for front in ref_frontiers:
        ref_frontiers_collar.append(frontiers_add_collar(front, collar))

    ref_union = make_union_frontiers(ref)
    hyp_union = make_union_frontiers(hyp)

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

    opt_size = max(ref_spkcount, hyp_spkcount)
    costs = np.zeros((opt_size, opt_size), dtype="float64")

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
            de[r, h] = (
                    ref_times[r] + miss_hyp[h] - efa[r, h] - emiss[r, h] - econf[r, h]
            )
            costs[r, h] = -round(de[r, h] * 1000)

    (map1, map2) = linear_sum_assignment(costs)
    map_rh = [-1] * ref_spkcount
    map_hr = [-1] * hyp_spkcount
    for i1 in range(0, opt_size):
        i = map1[i1]
        j = map2[i1]
        if (
                i < ref_spkcount
                and j < hyp_spkcount
                and de[i, j] > 0
                and tc[i, j] > 0
        ):
            map_rh[i] = j
            map_hr[j] = i

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

    best_segment_fix = None

    # Do one pass over the reference segments to see how much to gain if one hypothesis segment is corrected
    # Assume the speaker is correct if there's only one, or that the biggest is correct otherwise

    nf = len(ref_frontiers[0])
    for i in range(0, len(ref.speaker)):
        # segment boundaries
        st = ref.start_time[i]
        en = ref.end_time[i]

        # amount of silence before and after the segment
        silence_before = 0
        silence_after = 0
        for f in ref_union:
            if f[1] < st:
                silence_before = st - f[1] if f[0] == 'p' else 0
            if f[1] > en:
                silence_after = f[1] - en if f[0] == 'n' else 0
                break

        # scan the hypothesis, collate the per-speaker time
        hyptime = {}
        for j in range(0, len(hyp_frontiers)):
            hst = hyp.start_time[j]
            hen = hyp.end_time[j]
            if not (hen <= st or hst >= en):
                if hen > en:
                    hen = en
                if hst < st:
                    hst = st
                hspk = hyp.speaker[j]
                if hspk in hyptime:
                    hyptime[hspk] += hen - hst
                else:
                    hyptime[hspk] = hen - hst

        # compute the fixed time under the assumption that the longest speaker is correct
        fixed_time = 0
        if len(hyptime) > 1:
            best_time = 0
            for s in hyptime:
                tm = hyptime[s]
                if tm > best_time:
                    best_time = tm
                fixed_time += tm
            fixed_time -= best_time

        # compute the time in speech in the silences on the border, and the time in silence in the speech
        if len(hyp_union) > 0:
            stf = 0
            enf = len(hyp_union) - 1
            for j in range(0, len(hyp_union)):
                if hyp_union[j][1] < st:
                    stf = j
                if hyp_union[j][1] > en:
                    enf = j
                    break
            # pre/post-segment silence
            if hyp_union[stf][1] < st and hyp_union[stf][0] == 'n':
                sp = st - silence_before;
                if sp < hyp_union[stf][1]:
                    sp = hyp_union[stf][1]
                fixed_time += st - sp
            if hyp_union[enf][1] > en and hyp_union[enf][0] == 'p':
                sp = en + silence_after;
                if sp > hyp_union[enf][1]:
                    sp = hyp_union[enf][1]
                fixed_time += sp - en
            # in-segment silence
            sp = st
            for j in range(stf, enf + 1):
                if hyp_union[j][1] > st and hyp_union[j][0] == 'p':
                    sp = hyp_union[j][1]
                if hyp_union[j][1] > st and hyp_union[j][1] < en and hyp_union[j][0] == 'n':
                    fixed_time += hyp_union[j][1] - sp

        else:
            # nothing in the hypothesis, all the time is fixed
            fixed_time += en - st;
        if fixed_time:
            if (best_segment_fix == None) or (best_segment_fix[1] < fixed_time):
                best_segment_fix = [fixed_time, st, en]

    # find the couple of maximum confusion where both sides are mapped
    max_conf = 0
    max_conf_r = None
    max_conf_h = None
    for r in range(ref_spkcount):
        for h in range(hyp_spkcount):
            if confusion_matrix[r, h] > max_conf and map_rh[r] != -1 and map_hr[h] != -1:
                max_conf = confusion_matrix[r, h]
                max_conf_r = r
                max_conf_h = h
    if max_conf_r != None:
        # Of the two, pick the speaker with the maximum amount of error associated
        error_spk_ref = lost_ref[r]
        for h in range(hyp_spkcount):
            error_spk_ref += confusion_matrix[max_conf_r, h]
        error_spk_hyp = lost_hyp[h]
        for r in range(ref_spkcount):
            error_spk_hyp += confusion_matrix[r, max_conf_h]

        if (error_spk_ref > error_spk_hyp) or not correction_type[1]:
            # We want to pivot on the reference, that means merging the mapped hyp speaker and the mapped max error hyp speaker
            correct_point = find_common_point(ref_frontiers[max_conf_r], hyp_frontiers[map_rh[max_conf_r]])
            bad_point = find_common_point(ref_frontiers[max_conf_r], hyp_frontiers[max_conf_h])
            p1 = min(correct_point, bad_point)
            p2 = max(correct_point, bad_point)
            max_conf_a = Answer(True, "same", np.float32(p1), np.float32(p2))
            #max_conf_a = {"answer": {"value": True}, "response_type": "same", "time_1": np.float32(p1),
            #              "time_2": np.float32(p2)}
        elif (error_spk_hyp >= error_spk_ref) or not correction_type[0]:
            # We want to pivot on the hypothesis, that means splitting the mapped ref speaker and the mapped max error ref speaker
            correct_point = find_common_point(ref_frontiers[map_hr[max_conf_h]], hyp_frontiers[max_conf_h])
            bad_point = find_common_point(ref_frontiers[max_conf_r], hyp_frontiers[max_conf_h])
            #print(f"{correct_point} {bad_point}")
            p1 = min(correct_point, bad_point)
            p2 = max(correct_point, bad_point)
            max_conf_a = Answer(False, "same", np.float32(p1), np.float32(p2))
            #max_conf_a = {"answer": {"value": False}, "response_type": "same", "time_1": np.float32(p1),
            #              "time_2": np.float32(p2)}

    if (best_segment_fix == None and max_conf == 0) or (correction_type == (False, False, False)):
        #return {"answer": {"value": False}, "response_type": "stop", "time_1": np.float32(0.0),
        #        "time_2": np.float32(0.0)}
        return Answer(False, "stop", np.float32(0.0), np.float32(0.0))
    if best_segment_fix == None or max_conf > best_segment_fix[0] or not correction_type[2]:
        return max_conf_a
    else:
        #return {"answer": {"value": True}, "response_type": "boundary", "time_1": np.float32(best_segment_fix[1]),
        #        "time_2": np.float32(best_segment_fix[2])}
        return Answer(True, "boundary", np.float32(best_segment_fix[1]), np.float32(best_segment_fix[2]))


class UserSimulation:

    def __init__(self, parameters, correction_type=(True, True, True)):
        self.cost = 0
        self.max_cost_per_file = parameters["max_cost_per_file"]
        self.request_collar_cost = parameters["request_collar_cost"]
        self.correction_type = correction_type


    def compute_answer_cost(self, a):
        cost = 0
        #if a["response_type"] == "same":
        if a.response_type == "same":
            #time_1 = a["time_1"]
            #time_2 = a["time_2"]
            time_1 = a.time_1
            time_2 = a.time_2
            if abs(time_2 - time_1) >= self.request_collar_cost:
                cost += 2 * self.request_collar_cost
            else:
                cost += max(time_1, time_2) - min(time_1, time_2) + self.request_collar_cost
        elif a.response_type == "boundary":
            #elif a["response_type"] == "boundary":
            #time_1 = a["time_1"]
            #time_2 = a["time_2"]
            time_1 = a.time_1
            time_2 = a.time_2
            cost = time_2 - time_1 + self.request_collar_cost
        return cost

    def read(self, file_info, uem, reference):
        self.file_info = file_info
        self.reference = reference
        self.uem = uem

    def validate(self, message):
        answer = {}
#         print("entered validate:")
        #print(f"cost = {self.cost}, et max = {self.max_cost_per_file}")
        if self.cost >= self.max_cost_per_file:
            answer = Answer(False, "stop", 0.0, 0.0)
            #answer = {
            #    "answer": {"value": False},
            #    "response_type": "stop",
            #    "time_1": 0.0,
            #    "time_2": 0.0,
            #}
        elif message.file_info.supervision == "active":
            if message.system_request.request_type == "same":
                time_1 = message.system_request.time_1
                time_2 = message.system_request.time_2
                spk1 = self.find_speaker_for_time(time_1)
                spk2 = self.find_speaker_for_time(time_2)
                if abs(time_2 - time_1) >= self.request_collar_cost:
                    self.cost += 2 * self.request_collar_cost
                else:
                    self.cost += max(time_1, time_2) - min(time_1, time_2) + self.request_collar_cost
                print(
                    "USER: Check for same on %f (%s) vs. %f (%s)"
                    % (time_1, spk1, time_2, spk2)
                )
                #if spk1 ==None or spk2==None:
                #    import pdb
                #    pdb.set_trace()
                answer = Answer(spk1 == spk2, "same", time_1, time_2)
                #answer = {
                #    "answer": {"value": spk1 == spk2},
                #    "response_type": "same",
                #    "time_1": time_1,
                #    "time_2": time_2,
                #}
            elif message.system_request.request_type == "boundary":
                st, en = self.find_segment_for_time(message.system_request.time_1)
                if st != None:
                    self.cost += en - st + self.request_collar_cost
                    print(
                        "USER: Check for boundary on %f (%f - %f)"
                        % (message.system_request.time_1, st, en)
                    )
                    answer = Answer(True, "boundary", st, en )
                    #answer = {
                    #    "answer": {"value": True},
                    #    "response_type": "boundary",
                    #    "time_1": st,
                    #    "time_2": en,
                    #}
                else:
                    self.cost += self.request_collar_cost
                    print(
                        "USER: Check for boundary on %f (not speech)"
                        % (message.system_request.time_1)
                    )
                    answer = Answer(False, "boundary", 0.0, 0.0 )
                    #answer = {
                    #    "answer": {"value": False},
                    #    "response_type": "boundary",
                    #    "time_1": 0.0,
                    #    "time_2": 0.0,
                    #}

        elif message.file_info.supervision == "interactive":
            #print("Interactive model ON")
            answer = find_best_information(self.reference,
                                           message.hypothesis,
                                           0.250,
                                           correction_type=self.correction_type)

        else:
            answer = Answer(True, "stop", 0.0, 0.0 )
            #answer = {
            #    "response_type": 'stop',
            #    "time_1": np.float32(0),
            #    "time_2": np.float32(0),
            #    "answer": {"value": False},
            #}
        self.cost += self.compute_answer_cost(answer)
        #return answer['response_type'] != "stop", answer
        return answer.response_type != "stop", answer

    def find_segment_for_time(self, time):
        for i, s in enumerate(self.reference.speaker):
            if (
                    time >= self.reference.start_time[i]
                    and time < self.reference.end_time[i]
            ):
                return self.reference.start_time[i], self.reference.end_time[i]
        return None, None

    def find_speaker_for_time(self, time):
        for i, s in enumerate(self.reference.speaker):
            #            print(i, s, time, )
            if (
                    time >= self.reference.start_time[i]
                    and time < self.reference.end_time[i]
            ):
                return s
        return None


class Request:

    def __init__(self, request_type, time_1, time_2):
        self.request_type = request_type
        self.time_1 = time_1
        self.time_2 = time_2


class MessageToUser:

    def __init__(self, file_info, hypothesis, system_request):
        self.file_info = file_info
        self.hypothesis = hypothesis
        self.system_request = system_request

class Answer:

    def __init__(self, answer, response_type, time_1, time_2):
        self.answer = answer
        self.response_type = response_type
        self.time_1 = time_1
        self.time_2 = time_2

    def __repr__(self):
        return f"answer = {self.answer}\nresponse_type = {self.response_type}\ntime_1 = {self.time_1}\ntime_2 =  {self.time_2}"

class FileInfo:

    def __init__(self, file_id, supervision, time_stamp):
        self.file_id = file_id
        self.supervision = supervision
        self.time_stamp = time_stamp


class Reference:

    def __init__(self, speaker, start_time, end_time):
        self.speaker = speaker
        self.start_time = start_time
        self.end_time = end_time

    def to_diar(self, show):
        """
        Convert the Reference object into S4D DIAR object
        :return:
        """
        diar = s4d.Diar()
        for spk, start, stop in zip(self.speaker, self.start_time, self.end_time):
            diar.append(show = show,
                        cluster = spk,
                        cluster_type = 'speaker',
                        start = int(float(start) * 100),
                        stop = int(float(stop) * 100))

        return diar


class UEM:

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


    def to_diar(self, show):
        """
        Convert the UEM object into S4D DIAR object
        :return:
        """
        diar = s4d.Diar()
        for start, stop in zip(self.start_time, self.end_time):
            diar.append(show = show,
                        cluster = "uem",
                        start = int(float(start) * 100),
                        stop = int(float(stop) * 100))

        return diar


