#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ApplyBCI is a tool to compute charges from bond-charge increments.
# Copyright (C) 2015 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of ApplyBCI.
#
# ApplyBCI is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# ApplyBCI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
#--


import argparse
import numpy as np
from yaff import System, log, angstrom
from collections import namedtuple
log.set_level(log.silent)


def parse_arguments():
    '''Parse command-line arguments'''
    parser = argparse.ArgumentParser(description='Tool to compute charges with '
                                     'bond-charge increments')
    parser.add_argument('filename_system', metavar='XYZ',
                        help='an XYZ file with optionally '
                        'the cell parameters in the title line. The first nine numbers '
                        'encountered in the title line are interpreted as a_x, a_y, a_z, '
                        'b_x, b_y, b_z, c_x, c_y and c_z, respectively. Words that '
                        'can\'t be converted to real numbers are ignored. If less than '
                        'nine numbers are encountered, the system is assumed to be '
                        'aperiodic.')
    parser.add_argument('filename_rules', metavar='RULES',
                        help='A filename with atom type '
                        'rules. In-line comments start with a #. Empty lines are '
                        'ignored. On a non-empty line, the first word as the name of the '
                        'atom type. The rest of the line is a rule written in the '
                        'ATSELECT atom typing language.')
    parser.add_argument('filename_parameters', metavar='PARS',
                        help='A filename with charge '
                        'and bond-charge increment parameters. In-line comments start '
                        'with a #. Empty lines are ignored. Each line contains a '
                        'keyword, one or two atom types and one parameter. If the '
                        'keyword is CHARGE, one atom type is expected and the parameter '
                        'is just the partial charge for that atom type. When using the '
                        'CHARGE keyword, it is your responsibility to fix the total '
                        'charge of the system to the correct value. The BCI-12 keyword '
                        'expects two atom types and the parameter is increment. When two '
                        'atoms of the given types are bonded, the increment is added to '
                        'the charge of the atom of the first type and subtracted from '
                        'the second. BCI-13 is analogous to BCI-12 but works for all '
                        'pairs of atoms bonded to the same third atom, i.e. as in a '
                        'bending angle. The increments are super-imposed on top of the '
                        'charges set by the CHARGE keyword. The default charge of an '
                        'atom (before adding increments) is zero.')
    parser.add_argument('-d', '--decimals', nargs=1, type=float, default=4,
                        help='The number of decimals after the point to keep when '
                        'reading parameters and printing charges.')

    return parser.parse_args()


def load_system(fn):
    '''Load atomic numbers, coordinates and cell parameters from fn'''
    # Load the cell vectors from the second line.
    with open(fn) as f:
        # Skip one line.
        f.next()
        # Read rvecs (real-space cell vectors).
        real_numbers = []
        for word in f.next().split():
            try:
                real_numbers.append(float(word))
            except ValueError:
                pass
        print 'Detected %i real numbers in title line' % len(real_numbers)
        if len(real_numbers) >= 9:
            rvecs = np.array(real_numbers[:9]).reshape(3, 3)
            print 'Treating system as periodic with the following cell vectors in ' \
                  'Angstrom. Cell vectors are displayed as rows.'
            print rvecs
        else:
            print 'I\'m assuming the system is aperiodic because there are less than ' \
                  'nine real numbers in the title line.'
            rvecs = None
        print

    # Let Yaff read the file.
    return System.from_file(fn, rvecs=rvecs)


def words_without_comments(f):
    for iline, line in enumerate(f):
        # Strip comments and skip empty lines.
        words = line[:line.find('#')].split()
        if len(words) == 0:
            continue
        yield iline, words


def load_ffatypes(fn):
    '''Load atom type rules from fn.'''
    print 'Reading atom type rules'
    rules = []
    with open(fn) as f:
        for iline, words in words_without_comments(f):
            if len(words) < 2:
                raise IOError(('At least two words expected on line %i of atom types '
                               'file "%s". Got one.') % (iline, fn))

            # Recombine words into useful things.
            ffatype = words[0]
            rule = ''.join(words[1:])
            print '    %s  %s' % (ffatype.ljust(10), rule)

            # Add to the list
            rules.append((ffatype, rule))
    print
    return rules


def print_bonds_ffatypes(system):
    '''Print bond and atom type statistics on screen'''

    # Get all 13 pairs
    system.one_three_pairs = []
    for iatom0, iatom1s in system.neighs2.iteritems():
        for iatom1 in iatom1s:
            if iatom1 > iatom0:
                system.one_three_pairs.append((iatom0, iatom1))

    print 'Bond and atom type statistics'
    print '    Number of atoms:            %i' % system.natom
    print '    Number of bonds (12 pairs): %i' % system.nbond
    print '    Number of 13 pairs:         %i' % len(system.one_three_pairs)
    print '    Number of atoms by type:'
    for ffatype_id, ffatype in enumerate(system.ffatypes):
        print '        %s  %5i' % (ffatype.ljust(10), (system.ffatype_ids==ffatype_id).sum())

    def print_pair_stats(pairs):
        counts = {}
        for iatom0, iatom1 in pairs:
            key = tuple(sorted([system.ffatype_ids[iatom0], system.ffatype_ids[iatom1]]))
            counts[key] = counts.get(key, 0) + 1
        for key, count in sorted(counts.iteritems()):
            ffatype_id0, ffatype_id1 = key
            ffatype0 = system.ffatypes[ffatype_id0]
            ffatype1 = system.ffatypes[ffatype_id1]
            print '        %s  %s  %5i' % (ffatype0.ljust(10), ffatype1.ljust(10), count)

    print '    Number of bonds (12 pairs) by type:'
    print_pair_stats(system.bonds)
    print '    Number of 13 pairs by type:'
    print_pair_stats(system.one_three_pairs)


    print


def load_parameters(fn, decimals):
    '''Load charges and bci's from the parameter file fn.'''
    Parameters = namedtuple('Parameters', ['charges', 'bcis_12', 'bcis_13'])
    Keyword = namedtuple('Keyword', ['nffatype', 'dict'])

    charges = {}
    bcis_12 = {}
    bcis_13 = {}
    keywords = {
        'CHARGE': Keyword(1, charges),
        'BCI-12': Keyword(2, bcis_12),
        'BCI-13': Keyword(2, bcis_13),
    }
    print 'Reading parameters'
    strformat = '%%10.%if' % decimals
    with open(fn) as f:
        for iline, words in words_without_comments(f):
            # Parse a line with proper error handling.
            name = words[0].upper()
            keyword = keywords.get(name)
            if keyword is None:
                raise IOError('Unknown keyword "%s" on line %i of parameter file "%s".' %
                              (keyword, iline, fn))
            if len(words) != keyword.nffatype+2:
                raise IOError(('Incorrect number of words on line %i of parameter '
                               'file "%s". Expecting %i. Got %i') % (iline, fn,
                               keyword.nffatype + 2, len(words)))
            try:
                value = np.round(float(words[-1]), decimals)
            except ValueError:
                raise IOError(('Unreadable parameter "%s" on line %i of parameter file '
                               '"%s".') % (words[-1], iline, fn))
            # Store the data read from the line.
            key = tuple(words[1:-1])
            keyword.dict[key] = value
            print ('    %5s   %s  ' + strformat) % \
                  (name, '  '.join(w.ljust(10) for w in key), value)
            # Always assume anti-symmetry of the BCI parameters.
            if keyword.nffatype == 2:
                if key[0] == key[1]:
                    raise IOError(('BCI parameters must have different atom types on '
                                   'line %i of parameter file "%s".') % (iline, fn))
                key = key[::-1]
                value *= -1
                keyword.dict[key] = value

    print
    return Parameters(charges, bcis_12, bcis_13)


def compute_charges(system, parameters):
    '''Compute charges for the system using given parameters'''
    print 'Computing charges'

    print '    Setting charges according to CHARGE keywords'
    system.charges = np.zeros(system.natom)
    for iatom in xrange(system.natom):
        ffatype = system.get_ffatype(iatom)
        system.charges[iatom] = parameters.charges.get(ffatype, 0.0)
    print '        Total charge: %.10e' % system.charges.sum()

    def add_increments(system, pairs, bcis):
        for iatom0, iatom1 in pairs:
            ffatype0 = system.get_ffatype(iatom0)
            ffatype1 = system.get_ffatype(iatom1)
            increment = bcis.get((ffatype0, ffatype1), 0.0)
            system.charges[iatom0] += increment
            system.charges[iatom1] -= increment

    print '    Adding 12 increments'
    add_increments(system, system.bonds, parameters.bcis_12)
    print '        Total charge: %.10e' % system.charges.sum()

    print '    Adding 13 increments'
    add_increments(system, system.one_three_pairs, parameters.bcis_13)
    print '        Total charge: %.10e' % system.charges.sum()

    print


def print_structure(system, decimals):
    '''Print out the geometry and the charges'''
    print 'Atom types, coordinates (in Angstrom) and charges (in electron)'
    strformat = '%%10.%if' % decimals
    for iatom in xrange(system.natom):
        ffatype = system.get_ffatype(iatom)
        x, y, z = system.pos[iatom]/angstrom
        charge = system.charges[iatom]
        print ('    %10s  %10.4f  %10.4f  %10.4f  ' + strformat) % \
              (ffatype, x, y, z, charge)


def main():
    args = parse_arguments()

    # Load the system and detect bonds.
    system = load_system(args.filename_system)
    system.detect_bonds()

    # Load the atom typing rules and detect atom types.
    rules = load_ffatypes(args.filename_rules)
    system.detect_ffatypes(rules)

    # Print some information regarding atom types and bonds
    print_bonds_ffatypes(system)

    # load the parameters and compute charges.
    parameters = load_parameters(args.filename_parameters, args.decimals)
    compute_charges(system, parameters)

    # Print out five columns: atom type, x, y, z, charge. (Coordinates are in angstrom,
    # charges in electron.)
    print_structure(system, args.decimals)


if __name__ == '__main__':
    main()
