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
                        'CHARGE keyword, it is your responsability to fix the total '
                        'charge of the system to the correct value. The BCI-12 keyword '
                        'expects two atom types and the parameter is increment. When two '
                        'atoms of the given types are bonded, the increment is added to '
                        'the charge of the atom of the first type and subtracted from '
                        'the second. BCI-13 is analogous to BCI-12 but works for all '
                        'pairs of atoms bonded to the same third atom, i.e. as in a '
                        'bending angle. The increments are super-imposed on top of the '
                        'charges set by the CHARGE keyword. The default charge of an '
                        'atom (before adding increments) is zero.')
    parser.add_argument('-p', '--precision', nargs=1, type=float,
                        help='The precision with which the charges are printed.')

    return parser.parse_args()


def load_system(fn):
    '''Load atomic numbers, coordinates and cell parameters from fn'''
    # Load the cell vectors from the second line.
    with open(fn) as f:
        # Skip one line.
        f.next()
        # Read rvecs (real-space cell vectors).
        real_numbers = np.array([float(word) for word in f.next().split()
                                 if word.replace(".", "", 1).isdigit()])
        print 'Detected %i real numbers in title line' % len(real_numbers)
        if len(real_numbers) >= 9:
            rvecs = real_numbers[:9].reshape(3, 3)
            print 'Treating system as periodic with the following cell vectors in ' \
                  'Angstrom:'
            print rvecs
        else:
            print 'I\'m assuming the system is aperiodic because there are less than ' \
                  'nine real numbers in the title line.'
            rvecs = None
        print

    # Let Yaff read the file.
    from yaff import System, UnitCell
    return System.from_file(fn, rvecs=rvecs)


def load_ffatypes(fn):
    '''Load atom type rules from fn.'''
    print 'Reading atom types'
    rules = []
    with open(fn) as f:
        for line in f:
            # Strip comments and skip empty lines.
            words = line[:line.find('#')].split()
            if len(words) == 0:
                continue
            if len(words) < 2:
                raise IOError('Could not parse the following line from the atom types file:\n%s' % line[:-1])

            # Recombine words into useful things.
            ffatype = words[0]
            rule = ''.join(words[1:])
            print '  %10s %s' % (ffatype, rule)

            # Add to the list
            rules.append((ffatype, rule))
    return rules


def load_parameters(fn):
    '''Load charges and bci's from the parameter file fn.'''
    raise NotImplementedError


def compute_charges(system, parameters):
    '''Compute charges for the system using given parameters'''
    raise NotImplementedError


def print_structure(system):
    '''Print out the geometry and the charges'''
    raise NotImplementedError


def main():
    args = parse_arguments()

    # Load the system and detect bonds.
    system = load_system(args.filename_system)
    system.detect_bonds()

    # Load the atom typing rules and detect atom types.
    rules = load_ffatypes(args.filename_rules)
    system.detect_ffatypes(rules)

    # load the parameters and compute charges.
    parameters = load_parametes(args.filename_parameters, args.precision)
    compute_charges(system, parameters)

    # Print out five columns: atom type, x, y, z, charge. (Coordinates are in angstrom,
    # charges in electron.)
    print_structure(system, args.precision)


if __name__ == '__main__':
    main()
