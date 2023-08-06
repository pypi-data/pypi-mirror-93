"""
This module contains any class or function related with PELE's Impact
template.
"""

from copy import deepcopy

from simtk import unit

import peleffy
from peleffy.topology import ZMatrix


class Impact(object):
    """
    It is in charge of writing a Molecule object as a PELE's Impact
    template.
    """

    def __init__(self, topology):
        """
        Initializes an Impact object.

        Parameters
        ----------
        topology : a Topology object
            The molecular topology representation to write as a
            Impact template

        Examples
        --------

        Write the Impact template of a peleffy's molecule

        >>> from peleffy.topology import Molecule

        >>> molecule = Molecule('molecule.pdb')

        >>> from peleffy.forcefield import OpenForceField

        >>> openff = OpenForceField('openff_unconstrained-1.2.1.offxml')
        >>> parameters = openff.parameterize(molecule)

        >>> from peleffy.topology import Topology

        >>> topology = Topology(molecule, parameters)

        >>> from peleffy.template import Impact

        >>> impact = Impact(topology)
        >>> impact.to_file('molz')

        """

        # Check input parameters
        if (not isinstance(topology, peleffy.topology.Topology)
                and not
                isinstance(topology, peleffy.topology.topology.Topology)):
            raise TypeError('Invalid input molecule for Impact template')

        self._topology = deepcopy(topology)
        self._molecule = self._topology.molecule
        self._sort()

    def _get_absolute_parent_atom(self):
        """
        It returns the absolute parent atom of the Topology.

        Returns
        -------
        absolute_parent : a peleffy.topology.molecule.Atom
            The absolute parent atom corresponding to the Topology
        """
        for atom in self.topology.atoms:
            if atom.parent is None:
                return atom

        raise Exception('Topology has no absolut parent')

    def _get_core_atoms(self):
        """
        It returns all core atoms of the Topology.

        Returns
        -------
        core_atoms : list[Atom]
            The list of core atoms corresponding to the Topology
        """
        core_atoms = list()

        for atom in self.topology.atoms:
            if atom.core:
                core_atoms.append(atom)

        return core_atoms

    def _get_all_childs_of_atom(self, parent, child_location):
        """
        It returns all child atoms of the supplied Atom, if any.

        Parameters
        ----------
        parent : a peleffy.topology.molecule.Atom
            The Atom whose childs are requested
        child_location : str
            One of ['core', 'side chain']. Whether to look for childs
            in the core or the side chain

        Returns
        -------
        childs : list[Atom]
            The list of childs corresponding to the supplied Atom
        """
        childs = list()

        assert child_location in ['core', 'side chain'], \
            'Unexpected supplied child location'

        for atom in self.topology.atoms:
            if atom.parent == parent:
                if child_location == 'core' and atom.core:
                    childs.append(atom)
                elif child_location == 'side chain' and not atom.core:
                    childs.append(atom)

        return childs

    def _sort(self):
        """Sort and reindex atoms in a Molecule."""

        # Do not sort an empty array of atoms
        if len(self.topology.atoms) == 0:
            return

        sorted_atoms = list()

        # Sort core atoms by parent index
        absolute_parent = self._get_absolute_parent_atom()
        sorted_atoms.append(absolute_parent)
        added_new_child = True

        while added_new_child:
            added_new_child = False

            for atom in sorted_atoms:
                childs = self._get_all_childs_of_atom(
                    atom, child_location='core')

                for child in childs:
                    if child not in sorted_atoms:
                        sorted_atoms.append(child)
                        added_new_child = True

        # Sort non-core atoms by parent index
        added_new_child = True

        while added_new_child:
            added_new_child = False

            for atom in sorted_atoms:
                childs = self._get_all_childs_of_atom(
                    atom, child_location='side chain')

                for child in childs:
                    if child not in sorted_atoms:
                        sorted_atoms.append(child)
                        added_new_child = True

        # Define reindexer and reindex atoms
        reindexer = dict()
        for new_index, atom in enumerate(sorted_atoms):
            old_index = atom._index
            reindexer[old_index] = new_index
            atom.set_index(new_index)

        # Replace old atom list by the sorted one
        self.topology._atoms = sorted_atoms

        # Reindex bonds, angles, propers and impropers
        for bond in self.topology.bonds:
            bond.set_atom1_idx(reindexer[bond.atom1_idx])
            bond.set_atom2_idx(reindexer[bond.atom2_idx])
        for angle in self.topology.angles:
            angle.set_atom1_idx(reindexer[angle.atom1_idx])
            angle.set_atom2_idx(reindexer[angle.atom2_idx])
            angle.set_atom3_idx(reindexer[angle.atom3_idx])
        for proper in self.topology.propers:
            proper.set_atom1_idx(reindexer[proper.atom1_idx])
            proper.set_atom2_idx(reindexer[proper.atom2_idx])
            proper.set_atom3_idx(reindexer[proper.atom3_idx])
            proper.set_atom4_idx(reindexer[proper.atom4_idx])
        for improper in self.topology.impropers:
            improper.set_atom1_idx(reindexer[improper.atom1_idx])
            improper.set_atom2_idx(reindexer[improper.atom2_idx])
            improper.set_atom3_idx(reindexer[improper.atom3_idx])
            improper.set_atom4_idx(reindexer[improper.atom4_idx])

    def to_file(self, path):
        """
        It writes the Impact template to a file.

        Parameters
        ----------
        path : str
            Path to write to
        """
        with open(path, 'w') as file:
            self._write_header(file)
            self._write_resx(file)
            self._write_nbon(file)
            self._write_bond(file)
            self._write_thet(file)
            self._write_phi(file)
            self._write_iphi(file)
            self._write_end(file)

    def _write_header(self, file):
        """
        It writes the header of the Impact file.

        Parameters
        ----------
        file : file object
            File to write to
        """
        file.write('* LIGAND DATABASE FILE')
        file.write(' ({})'.format(self.topology.parameters.forcefield_name))
        file.write('\n')
        file.write('* File generated with peleffy-{}\n'.format(
            peleffy.__version__))
        file.write('*\n')

    def _write_resx(self, file):
        """
        It writes the resx section of the Impact file.

        Parameters
        ----------
        file : file object
            File to write to
        """
        # template name
        file.write('{:5}'.format(self.molecule.tag))
        # number of non bonding parameters
        file.write('{:6d}'.format(len(self.topology.atoms)))
        # number of bond parameters
        file.write('{:6d}'.format(len(self.topology.bonds)))
        # number of angle parameters
        file.write('{:6d}'.format(len(self.topology.angles)))
        # number of dihedral parameters
        # TODO doublecheck that it is indeed the sum of propers and impropers
        file.write('{:8d}'.format(len(self.topology.propers)
                                  + len(self.topology.impropers)))
        # # number of non-null elements in the interactions matrix
        # TODO It might not be always 0
        file.write('{:8d}'.format(0))
        file.write('\n')

        zmatrix = ZMatrix(self.topology)

        for i, atom in enumerate(self.topology.atoms):
            w_atom = WritableAtom(atom)
            # atom id number
            file.write('{:5d}'.format(w_atom.index))
            file.write(' ')
            file.write('{:5d}'.format(w_atom.parent.index))
            file.write(' ')
            file.write('{:1}'.format(w_atom.core))
            file.write('  ')
            file.write('{:4}'.format(w_atom.OPLS_type))
            file.write('  ')
            file.write('{:4}'.format(w_atom.PDB_name))
            file.write(' ')
            file.write('{:5}'.format(w_atom.unknown))
            file.write(' ')
            file.write('{: 11.6f}'.format(zmatrix[i][0]))
            file.write(' ')
            file.write('{: 11.6f}'.format(zmatrix[i][1]))
            file.write(' ')
            file.write('{: 11.6f}'.format(zmatrix[i][2]))
            file.write('\n')
        # TODO Should we add the interactions matrix here?

    def _write_nbon(self, file):
        """
        It writes the nbon section of the Impact file.

        Parameters
        ----------
        file : file object
            File to write to
        """
        file.write('NBON\n')
        for atom in self.topology.atoms:
            w_atom = WritableAtom(atom)
            # TODO an extra space is found in the IMPACT file generated by
            # PlopRotTemp, consider removing it
            file.write(' ')
            # Atom id
            file.write('{:5d}'.format(w_atom.index))
            file.write(' ')
            # Sigma
            file.write('{: 8.4f}'.format(w_atom.sigma))
            file.write(' ')
            # Epsilon
            file.write('{: 8.4f}'.format(w_atom.epsilon))
            file.write(' ')
            # Charge
            file.write('{: 10.6f}'.format(w_atom.charge))
            file.write(' ')
            # Rad. Non Polar SGB
            file.write('{: 8.4f}'.format(w_atom.born_radius))
            file.write(' ')
            # Rad. Non Polar Type
            file.write('{: 8.4f}'.format(w_atom.SASA_radius))
            file.write(' ')
            # SGB Non Polar gamma
            file.write('{: 13.9f}'.format(w_atom.nonpolar_gamma))
            file.write(' ')
            # SGB Non Polar type
            file.write('{: 13.9f}'.format(w_atom.nonpolar_alpha))
            file.write('\n')

    def _write_bond(self, file):
        """
        It writes the bond section of the Impact file.

        Parameters
        ----------
        file : file object
            File to write to
        """
        file.write('BOND\n')
        for bond in self.topology.bonds:
            w_bond = WritableBond(bond)
            idx1, idx2, spring, eq_dist = [attr[1] for attr in list(w_bond)]
            # TODO an extra space is found in the IMPACT file generated by
            # PlopRotTemp, consider removing it
            file.write(' ')
            # Atom 1 id
            file.write('{:5d}'.format(idx1))
            file.write(' ')
            # Atom 2 id
            file.write('{:5d}'.format(idx2))
            file.write(' ')
            # Spring constant
            file.write('{: 9.3f}'.format(spring))
            file.write(' ')
            # Equilibrium distance
            file.write('{: 6.3f}\n'.format(eq_dist))

    def _write_thet(self, file):
        """
        It writes the thet section of the Impact file.

        Parameters
        ----------
        file : file object
            File to write to
        """
        file.write('THET\n')
        for angle in self.topology.angles:
            w_angle = WritableAngle(angle)
            idx1, idx2, idx3, spring, eq_angl = [attr[1] for attr in
                                                 list(w_angle)]
            # TODO an extra space is found in the IMPACT file generated by
            # PlopRotTemp, consider removing it
            file.write(' ')
            # Atom 1 id
            file.write('{:5d}'.format(idx1))
            file.write(' ')
            # Atom 2 id
            file.write('{:5d}'.format(idx2))
            file.write(' ')
            # Atom 3 id
            file.write('{:5d}'.format(idx3))
            file.write(' ')
            # Spring constant
            file.write('{: 11.5f}'.format(spring))
            # Equilibrium angle
            file.write('{: 11.5f}\n'.format(eq_angl))

    def _write_phi(self, file):
        """
        It writes the phi section of the Impact file.

        Parameters
        ----------
        file : file object
            File to write to
        """
        file.write('PHI\n')
        for proper in self.topology.propers:
            w_proper = WritableProper(proper)
            idx1, idx2, idx3, idx4, constant, prefactor, term, phase = \
                [attr[1] for attr in list(w_proper)]
            # Atom 1 id
            file.write('{:5d}'.format(idx1))
            file.write(' ')
            # Atom 2 id
            file.write('{:5d}'.format(idx2))
            file.write(' ')
            # Atom 3 id
            file.write('{:5d}'.format(idx3))
            file.write(' ')
            # Atom 4 id
            file.write('{:5d}'.format(idx4))
            file.write(' ')
            # Constant
            file.write('{: 9.5f}'.format(constant))
            file.write(' ')
            # Prefactor
            file.write('{: 4.1f}'.format(prefactor))
            file.write(' ')
            # Number of term
            file.write('{:3.1f}'.format(term))
            # Phase (only if different from 0)
            if phase != 0.0:
                file.write(' ')
                file.write('{:5.1f}'.format(phase))
            file.write('\n')

    def _write_iphi(self, file):
        """
        It writes the iphi section of the Impact file.

        Parameters
        ----------
        file : file object
            File to write to
        """
        file.write('IPHI\n')
        for improper in self.topology.impropers:
            w_improper = WritableImproper(improper)
            idx1, idx2, idx3, idx4, constant, prefactor, term = \
                [attr[1] for attr in list(w_improper)]
            # TODO an extra space is found in the IMPACT file generated by
            # PlopRotTemp, consider removing it
            file.write(' ')
            # Atom 1 id
            file.write('{:5d}'.format(idx1))
            file.write(' ')
            # Atom 2 id
            file.write('{:5d}'.format(idx2))
            file.write(' ')
            # Atom 3 id
            file.write('{:5d}'.format(idx3))
            file.write(' ')
            # Atom 4 id
            file.write('{:5d}'.format(idx4))
            file.write(' ')
            # Constant
            file.write('{: 9.5f}'.format(constant))
            file.write(' ')
            # Prefactor
            file.write('{: 4.1f}'.format(prefactor))
            file.write(' ')
            # Number of term
            file.write('{:3.1f}'.format(term))
            file.write('\n')

    def _write_end(self, file):
        """
        It writes the ending line of the Impact file.

        Parameters
        ----------
        file : file object
            File to write to
        """
        file.write('END\n')

    @property
    def molecule(self):
        """
        The peleffy's Molecule.

        Returns
        -------
        molecule : a peleffy.topology.Molecule
            The peleffy's Molecule object
        """
        return self._molecule

    @property
    def topology(self):
        """
        The peleffy's Topology.

        Returns
        -------
        topology : a peleffy.topology.Topology
            The peleffy's Topology object
        """
        return self._topology


class WritableWrapper(object):
    """
    Wrapper class for writable parameters.
    """

    @staticmethod
    def none_to_zero(f):
        """
        It converts a returned None to zero.

        Parameters
        ----------
        f : function
            The function to apply the decorator to

        Returns
        -------
        out : function's output
            It is set to zero in case that it is None
        """
        def function_wrapper(*args, **kwargs):
            out = f(*args, **kwargs)
            if out is None:
                out = int(0)
            return out
        return function_wrapper

    @staticmethod
    def dummy_to_writable(f):
        """
        It converts a returned DummyAtom to a WritableAtom.

        Parameters
        ----------
        f : function
            The function to apply the decorator to

        Returns
        -------
        out : WritableAtom
            A WritableAtom object
        """
        def function_wrapper(*args, **kwargs):
            out = f(*args, **kwargs)
            out = WritableAtom(out)
            return out
        return function_wrapper

    @staticmethod
    def none_to_dummy(f):
        """
        It converts a returned None to a DummyAtom.

        Parameters
        ----------
        f : function
            The function to apply the decorator to

        Returns
        -------
        out : DummyAtom
            A DummyAtom object
        """
        def function_wrapper(*args, **kwargs):
            out = f(*args, **kwargs)
            if out is None:
                out = peleffy.topology.elements.DummyAtom(index=-1)
            return out
        return function_wrapper

    @staticmethod
    def in_angstrom(f):
        """
        It expresses a simtk.unit.Quantity in angstroms.

        Parameters
        ----------
        f : function
            The function to apply the decorator to

        Returns
        -------
        out : float
            simtk.unit.Quantity expressed in angstroms
        """
        def function_wrapper(*args, **kwargs):
            out = f(*args, **kwargs)
            return out.value_in_unit(unit.angstrom)
        return function_wrapper

    @staticmethod
    def in_kcalmol(f):
        """
        It expresses a simtk.unit.Quantity in kcal/mol.

        Parameters
        ----------
        f : function
            The function to apply the decorator to

        Returns
        -------
        out : float
            simtk.unit.Quantity expressed in kcal/mol
        """
        def function_wrapper(*args, **kwargs):
            out = f(*args, **kwargs)
            return out.value_in_unit(unit.kilocalorie / unit.mole)
        return function_wrapper

    @staticmethod
    def in_elementarycharge(f):
        """
        It expresses a simtk.unit.Quantity in elementary charges.

        Parameters
        ----------
        f : function
            The function to apply the decorator to

        Returns
        -------
        out : float
            simtk.unit.Quantity expressed in elementary charges
        """
        def function_wrapper(*args, **kwargs):
            out = f(*args, **kwargs)
            return out.value_in_unit(unit.elementary_charge)
        return function_wrapper

    @staticmethod
    def in_kcal_rad2mol(f):
        """
        It expresses a simtk.unit.Quantity in kcal/rad2mol.

        Parameters
        ----------
        f : function
            The function to apply the decorator to

        Returns
        -------
        out : float
            simtk.unit.Quantity expressed in kcal/rad2mol
        """
        def function_wrapper(*args, **kwargs):
            out = f(*args, **kwargs)
            return out.value_in_unit(unit.kilocalorie
                                     / (unit.radian**2 * unit.mole))
        return function_wrapper

    @staticmethod
    def in_deg(f):
        """
        It expresses a simtk.unit.Quantity in degrees.

        Parameters
        ----------
        f : function
            The function to apply the decorator to

        Returns
        -------
        out : float
            simtk.unit.Quantity expressed in degrees
        """
        def function_wrapper(*args, **kwargs):
            out = f(*args, **kwargs)
            return out.value_in_unit(unit.degree)
        return function_wrapper

    @staticmethod
    def in_kcal_angstrom2mol(f):
        """
        It expresses a simtk.unit.Quantity in kcal/angstrom2mol.

        Parameters
        ----------
        f : function
            The function to apply the decorator to

        Returns
        -------
        out : float
            simtk.unit.Quantity expressed in kcal/angstrom2mol
        """
        def function_wrapper(*args, **kwargs):
            out = f(*args, **kwargs)
            return out.value_in_unit(unit.kilocalorie
                                     / (unit.angstrom**2 * unit.mole))
        return function_wrapper


class WritableAtom(peleffy.topology.Atom, WritableWrapper):
    """
    Writable peleffy's Atom class
    """

    def __init__(self, atom):
        """
        It initializes a WritableAtom object.

        Parameters
        ----------
        atom : a peleffy.topology.molecule.Atom
            The Atom to create the WritableAtom with
        """
        # We do not want to modify the original object
        atom = deepcopy(atom)

        assert isinstance(atom, (peleffy.topology.Atom,
                                 peleffy.topology.elements.Atom,
                                 peleffy.topology.elements.DummyAtom)), \
            'Wrong type: {}'.format(type(atom))

        super().__init__(atom.index, atom.core, atom.OPLS_type, atom.PDB_name,
                         atom.unknown, atom.x, atom.y, atom.z, atom.sigma,
                         atom.epsilon, atom.charge, atom.born_radius,
                         atom.SASA_radius, atom.nonpolar_gamma,
                         atom.nonpolar_alpha, atom.parent)

    @property
    @WritableWrapper.dummy_to_writable
    @WritableWrapper.none_to_dummy
    def parent(self):
        """
        Atom's parent.

        Returns
        -------
        parent : a peleffy.topology.molecule.Atom
            The parent of this Atom object
        """
        return super().parent

    @property
    def index(self):
        """
        Atom's index.

        Returns
        -------
        index : int
            The index of this Atom object
        """
        return int(self._index) + 1

    @property
    def core(self):
        """
        Atom's core char.

        Returns
        -------
        index : str
            The core type of this Atom object
        """
        if self._core:
            return 'M'
        else:
            return 'S'

    @property
    def OPLS_type(self):
        """
        Atom's OPLS type.

        .. todo ::

           * Consider removing any reference to OPLS, if possible
             Otherwise, use SMIRks to find the best match

        Returns
        -------
        index : str
            The OLPS type of this Atom object
        """
        return super().OPLS_type  # stands for OpenForceField type

    # TODO
    @property
    @WritableWrapper.none_to_zero
    def unknown(self):
        """
        Atom's unknown int.

        .. todo ::

           * Review the actual purpose of this attribute in PELE

        Returns
        -------
        unknown : int
            The unknown int of this Atom object
        """
        return super().unknown

    @property
    @WritableWrapper.in_angstrom
    def sigma(self):
        """
        Atom's sigma.

        Returns
        -------
        sigma : float
            The sigma of this Atom object, expressed in angstroms
        """
        return super().sigma

    @property
    @WritableWrapper.in_kcalmol
    def epsilon(self):
        """
        Atom's epsilon.

        Returns
        -------
        epsilon : float
            The epsilon of this Atom object, expressed in kcal/mol
        """
        return super().epsilon

    @property
    @WritableWrapper.in_elementarycharge
    def charge(self):
        """
        Atom's charge.

        Returns
        -------
        charge : float
            The charge of this Atom object, expressed in elementary units
        """
        return super().charge

    @property
    @WritableWrapper.in_angstrom
    def born_radius(self):
        """
        Atom's Born radius.

        Returns
        -------
        born_radius : float
            The Born radius of this Atom object
        """
        if super().born_radius is None:
            return unit.Quantity(0, unit.angstroms)

        return super().born_radius

    @property
    @WritableWrapper.in_angstrom
    def SASA_radius(self):
        """
        Atom's SASA radius.

        Returns
        -------
        SASA_radius : float
            The SASA radius of this Atom object, expressed in angstroms
        """
        return super().SASA_radius

    @property
    @WritableWrapper.none_to_zero
    def nonpolar_gamma(self):
        """
        Atom's nonpolar gamma.

        Returns
        -------
        nonpolar_gamma : float
            The nonpolar gamma of this Atom object
        """
        return super().nonpolar_gamma

    @property
    @WritableWrapper.none_to_zero
    def nonpolar_alpha(self):
        """
        Atom's nonpolar alpha.

        Returns
        -------
        nonpolar_alpha : float
            The nonpolar alpha of this Atom object
        """
        return super().nonpolar_alpha


class WritableBond(peleffy.topology.Bond, WritableWrapper):
    """
    Writable peleffy's Bond class
    """

    def __init__(self, bond):
        """
        It initializes a WritableBond object.

        Parameters
        ----------
        bond : a peleffy.topology.Bond
            The Bond to create the WritableBond with
        """
        # We do not want to modify the original object
        bond = deepcopy(bond)

        assert isinstance(bond, (peleffy.topology.Bond,
                                 peleffy.topology.elements.Bond)), \
            'Wrong type: {}'.format(type(bond))

        super().__init__(index=bond.index, atom1_idx=bond.atom1_idx,
                         atom2_idx=bond.atom2_idx,
                         spring_constant=bond.spring_constant,
                         eq_dist=bond.eq_dist)

    @property
    def atom1_idx(self):
        """
        Bond's atom1 index.

        Returns
        -------
        atom1_idx : int
            The index of the first atom involved in this Bond object
        """
        return super().atom1_idx + 1

    @property
    def atom2_idx(self):
        """
        Bond's atom2 index.

        Returns
        -------
        atom2_idx : int
            The index of the second atom involved in this Bond object
        """
        return super().atom2_idx + 1

    @property
    @WritableWrapper.in_kcal_angstrom2mol
    def spring_constant(self):
        """
        Bond's spring constant.

        Returns
        -------
        spring_constant : float
            The spring constant of this Bond object
        """
        return super().spring_constant

    @property
    @WritableWrapper.in_angstrom
    def eq_dist(self):
        """
        Bond's equilibrium distance.

        Returns
        -------
        eq_dist : float
            The equilibrium distance of this Bond object
        """
        return super().eq_dist


class WritableAngle(peleffy.topology.Angle, WritableWrapper):
    """
    Writable peleffy's Angle class
    """

    def __init__(self, angle):
        """
        It initializes a WritableAngle object.

        Parameters
        ----------
        angle : a peleffy.topology.Angle
            The Angle to create the WritableAngle with
        """
        # We do not want to modify the original object
        angle = deepcopy(angle)

        assert isinstance(angle, (peleffy.topology.Angle,
                                  peleffy.topology.elements.Angle)), \
            'Wrong type: {}'.format(type(angle))

        super().__init__(index=angle.index, atom1_idx=angle.atom1_idx,
                         atom2_idx=angle.atom2_idx, atom3_idx=angle.atom3_idx,
                         spring_constant=angle.spring_constant,
                         eq_angle=angle.eq_angle)

    @property
    def atom1_idx(self):
        """
        Angle's atom1 index.

        Returns
        -------
        atom1_idx : int
            The index of the first atom involved in this Angle object
        """
        return super().atom1_idx + 1

    @property
    def atom2_idx(self):
        """
        Angle's atom2 index.

        Returns
        -------
        atom2_idx : int
            The index of the second atom involved in this Angle object
        """
        return super().atom2_idx + 1

    @property
    def atom3_idx(self):
        """
        Angle's atom3 index.

        Returns
        -------
        atom3_idx : int
            The index of the third atom involved in this Angle object
        """
        return super().atom3_idx + 1

    @property
    @WritableWrapper.in_kcal_rad2mol
    def spring_constant(self):
        """
        Angle's spring constant.

        Returns
        -------
        spring_constant : float
            The spring constant of this Angle object
        """
        return super().spring_constant

    @property
    @WritableWrapper.in_deg
    def eq_angle(self):
        """
        Angle's equilibrium distance.

        Returns
        -------
        eq_angle : float
            The equilibrium angle of this Angle object
        """
        return super().eq_angle


class WritableProper(peleffy.topology.Proper, WritableWrapper):
    """
    Writable peleffy's Proper class
    """

    def __init__(self, proper):
        """
        It initializes a WritableProper object.

        Parameters
        ----------
        proper : a peleffy.topology.Proper
            The Proper to create the WritableProper with
        """
        # We do not want to modify the original object
        proper = deepcopy(proper)

        assert isinstance(proper, (peleffy.topology.Proper,
                                   peleffy.topology.elements.Proper)), \
            'Wrong type: {}'.format(type(proper))

        super().__init__(index=proper.index, atom1_idx=proper.atom1_idx,
                         atom2_idx=proper.atom2_idx,
                         atom3_idx=proper.atom3_idx,
                         atom4_idx=proper.atom4_idx,
                         periodicity=proper.periodicity,
                         prefactor=proper.prefactor,
                         constant=proper.constant,
                         phase=proper.phase)

        self.exclude = proper.exclude

    @property
    def atom1_idx(self):
        """
        Proper's atom1 index.

        Returns
        -------
        atom1_idx : int
            The index of the first atom involved in this Proper object
        """
        return super().atom1_idx + 1

    @property
    def atom2_idx(self):
        """
        Proper's atom2 index.

        Returns
        -------
        atom2_idx : int
            The index of the second atom involved in this Proper object
        """
        return super().atom2_idx + 1

    @property
    def atom3_idx(self):
        """
        Proper's atom3 index.

        Returns
        -------
        atom3_idx : int
            The index of the third atom involved in this Proper object
        """
        if self.exclude:
            return (super().atom3_idx + 1) * -1
        else:
            return super().atom3_idx + 1

    @property
    def atom4_idx(self):
        """
        Proper's atom4 index.

        Returns
        -------
        atom4_idx : int
            The index of the fourth atom involved in this Proper object
        """
        return super().atom4_idx + 1

    @property
    @WritableWrapper.in_kcalmol
    def constant(self):
        """
        Proper's constant.

        Returns
        -------
        constant : float
            The constant of this Proper object, expressed in kcal/mol
        """
        return super().constant

    @property
    @WritableWrapper.in_deg
    def phase(self):
        """
        Proper's phase constant.

        Returns
        -------
        phase : float
            The phase constant of this Proper object, expressed in
            degrees
        """
        return super().phase


class WritableImproper(peleffy.topology.Improper, WritableWrapper):
    """
    Writable peleffy's Improper class
    """

    def __init__(self, improper):
        """
        It initializes a WritableImproper object.

        Parameters
        ----------
        improper : a peleffy.topology.Improper
            The Improper to create the WritableImproper with
        """
        # We do not want to modify the original object
        improper = deepcopy(improper)

        assert isinstance(improper, (peleffy.topology.Improper,
                                     peleffy.topology.elements.Improper)), \
            'Wrong type: {}'.format(type(improper))

        super().__init__(index=improper.index, atom1_idx=improper.atom1_idx,
                         atom2_idx=improper.atom2_idx,
                         atom3_idx=improper.atom3_idx,
                         atom4_idx=improper.atom4_idx,
                         periodicity=improper.periodicity,
                         prefactor=improper.prefactor,
                         constant=improper.constant)

    @property
    def atom1_idx(self):
        """
        Improper's atom1 index.

        Returns
        -------
        atom1_idx : int
            The index of the first atom involved in this Improper object
        """
        return super().atom1_idx + 1

    @property
    def atom2_idx(self):
        """
        Improper's atom2 index.

        Returns
        -------
        atom2_idx : int
            The index of the second atom involved in this Improper object
        """
        return super().atom2_idx + 1

    @property
    def atom3_idx(self):
        """
        Improper's atom3 index.

        Returns
        -------
        atom3_idx : int
            The index of the third atom involved in this Improper object
        """
        return super().atom3_idx + 1

    @property
    def atom4_idx(self):
        """
        Improper's atom4 index.

        Returns
        -------
        atom4_idx : int
            The index of the fourth atom involved in this Improper object
        """
        return super().atom4_idx + 1

    @property
    @WritableWrapper.in_kcalmol
    def constant(self):
        """
        Improper's constant.

        Returns
        -------
        constant : float
            The constant of this Improper object, expressed in kcal/mol
        """
        return super().constant
