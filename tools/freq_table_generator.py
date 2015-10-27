#!/usr/bin/python
# ----------------------------------------------------------------------------
# Frequency table generator - riq
# ----------------------------------------------------------------------------
'''
Multiplying Table Generator
'''
from __future__ import division, unicode_literals, print_function
import sys
import os
import getopt


__docformat__ = 'restructuredtext'

__freqs = []
__sid_notes = []


def print_note(hi, o, s, steps):
    if s is not 0:
        sys.stdout.write(",")
    if hi:
        sys.stdout.write("$%02x" % (int(round(__sid_notes[s + o * steps])) >> 8))
    else:
        sys.stdout.write("$%02x" % (int(round(__sid_notes[s + o * steps])) & 0xff))


def run(basefreq, octaves, steps, phi, debug):
    # print 8 elements per line
    sys.stdout.write('; autogenerated table: %s -b%d -o%d -s%d %d\n' % (os.path.basename(sys.argv[0]), basefreq, octaves, steps, phi))

    constant = (256 ** 3) / phi

    for o in range(0, octaves):
        for s in range(0, steps):
            # +3 , since it stars with C, not A
            # -5, since it starts 5 octaves below
            note = ((o-5) * steps) + 3 + s
            freq = basefreq * 2 ** (note / steps)
            __freqs.append(freq)
            sid_note = freq * constant
            if sid_note > 0xffff:
                sid_note = 0xffff
            __sid_notes.append(sid_note)

    if debug:
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        sys.stdout.write("Debug\n")
        for i in range(0, octaves * steps):
            print("%d - %s\t%8.2f\t$%04x" % (i/steps, notes[i % len(notes)], __freqs[i], int(round(__sid_notes[i]))))

    else:
        sys.stdout.write("freq_table_lo:\n")
        for o in range(0, octaves):
            sys.stdout.write(".byte ")
            for i in range(0, steps):
                print_note(False, o, i, steps)
            sys.stdout.write("  ; %d\n" % o)

        sys.stdout.write("freq_table_hi:\n")
        for o in range(0, octaves):
            sys.stdout.write(".byte ")
            for i in range(0, steps):
                print_note(True, o, i, steps)
            sys.stdout.write("  ; %d\n" % o)


def help():
    print("%s v0.1 - An utility to generate SID frequency tables" % os.path.basename(sys.argv[0]))
    print("\nUsage: %s [options] pal|ntsc|paln|phi" % os.path.basename(sys.argv[0]))
    print("\t-b base_freq\t\t\tDefault=440")
    print("\t-o octaves\t\t\tDefault=8")
    print("\t-s steps_per_octave\t\tDefault=12")
    print("\t-f only prints pure frequency values. Not SID notes")
    print("\nUse a phi of 985248 for PAL, 1022727 for NTSC and 1023440 for PAL-N (Drean)")
    print("\nExamples:")
    print("\t%s -o8 -s12 985248" % os.path.basename(sys.argv[0]))
    print("\t%s 1022727" % os.path.basename(sys.argv[0]))
    print("\t%s 1023440" % os.path.basename(sys.argv[0]))
    print("\t%s pal" % os.path.basename(sys.argv[0]))
    print("\t%s ntsc" % os.path.basename(sys.argv[0]))
    sys.exit(-1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        help()

    octaves = 8
    steps = 12
    phi = 985248
    basefreq = 440
    debug = False

    d = {'pal': 985248,
         'ntsc': 1022727,
         'paln': 1023440
        }

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "b:o:s:d", ["basefreq=", "octaves=", "steps=", "debug"])
        for opt, arg in opts:
            if opt in ("-o", "--octaves"):
                octaves = int(arg)
            elif opt in ("-s", "--steps"):
                steps = int(arg)
            elif opt in ("-b", "--basefreq"):
                basefreq = int(arg)
            elif opt in ("-d", "--debug"):
                debug = True
        if not len(args) == 1:
            help()
        else:
            if args[0] in d:
                phi = d[args[0]]
            else:
                phi = int(args[0])
    except getopt.GetoptError, e:
        print(e)

    run(basefreq, octaves, steps, phi, debug)
