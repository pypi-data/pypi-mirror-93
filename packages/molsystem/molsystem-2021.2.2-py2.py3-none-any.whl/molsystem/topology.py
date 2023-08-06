# -*- coding: utf-8 -*-

"""Topological methods for the system"""

import logging

try:
    from openbabel import openbabel
except ModuleNotFoundError:
    print(
        'Please install openbabel using conda:\n'
        '     conda install -c conda-forge openbabel'
    )
    raise

logger = logging.getLogger(__name__)


class TopologyMixin:
    """A mixin for handling topology in a configuration."""

    def find_molecules(self, as_indices=False):
        """Find the separate molecules.

        Parameters
        ----------
        as_indices : bool = False
            Whether to return 0-based indices (True) or atom ids (False)

        Returns
        -------
        molecules : [[int]*n_molecules]
            A list of lists of atom ids or indices for the molecules
        """

        molecules = []

        atoms = self.atoms
        atom_ids = atoms.ids
        n_atoms = len(atom_ids)

        if n_atoms == 0:
            return molecules

        to_index = {j: i for i, j in enumerate(atom_ids)}
        neighbors = self.bonded_neighbors()
        visited = [False] * n_atoms
        while True:
            # Find first atom not yet visited
            try:
                index = visited.index(False)
            except ValueError:
                break
            visited[index] = True
            i = atom_ids[index]
            atoms = [i]
            next_atoms = neighbors[i]
            while len(next_atoms) > 0:
                tmp = []
                for i in next_atoms:
                    if not visited[to_index[i]]:
                        atoms.append(i)
                        visited[to_index[i]] = True
                        tmp.extend(neighbors[i])
                next_atoms = tmp
            molecules.append(sorted(atoms))
        if as_indices:
            return [[to_index[j] for j in js] for js in molecules]
        else:
            return molecules

    def bonded_neighbors(self, as_indices=False, first_index=0):
        """The atoms bonded to each atom in the system.

        Parameters
        ----------
        as_indices : bool = False
            Whether to return 0-based indices (True) or atom ids (False)
        first_index : int = 0
            The smallest index, e.g. 0 or 1

        Returns
        -------
        neighbors : {int: [int]} or [[int]] for indices
            list of atom ids for each atom id
        """
        neighbors = {}

        atoms = self.atoms
        bonds = self.bonds
        n_atoms = atoms.n_atoms

        if n_atoms == 0:
            if as_indices:
                return []
            else:
                return neighbors

        atom_ids = atoms.ids
        neighbors = {i: [] for i in atom_ids}

        if bonds.n_bonds > 0:
            for bond in bonds.bonds():
                i = bond['i']
                j = bond['j']
                neighbors[i].append(j)
                neighbors[j].append(i)

        if as_indices:
            # Convert to indices
            to_index = {j: i + first_index for i, j in enumerate(atom_ids)}
            result = [[]] * (n_atoms + first_index)
            for i, js in neighbors.items():
                result[to_index[i]] = sorted([to_index[j] for j in js])
            return result
        else:
            for i in neighbors:
                neighbors[i].sort()

            return neighbors

    def create_molecule_subsets(self):
        """Create a subset for each molecule in a configuration.

        Returns
        -------
        [int]
            The ids of the subsets, one per molecule.
        """
        # Find the molecules and the create the subsets if they don't exist.
        molecules = self.find_molecules()

        # Remove any previous subsets for this configuration
        subsets = self['subset']
        tid = 1
        sids = subsets.find(tid)
        if len(sids) > 0:
            subsets.delete(sids)

        # Now create the new set.
        sids = []
        for atom_ids in molecules:
            sid = subsets.create(tid, atoms=atom_ids)
            sids.append(sid)

        return sids

    def create_molecule_templates(
        self, full_templates=True, create_subsets=True
    ):
        """Create a template for each unique molecule in a configuration.

        By default also create subsets linking each template to the atoms
        of the molecules in the system.

        Parameters
        ----------
        full_templates : bool = True
            If true, create full templates by creating systems for the
            molecules.
        create_subsets : bool = True
            If true, create subsets linking the templates to the molecules.

        Returns
        -------
        [int] or [[int], [int]]
            The ids of the templates, or if create_subsets is True
            a two-element list containing the list of templates and
            list of subsets.
        """
        templates = self.system_db.templates

        # Find the molecules
        molecules = self.find_molecules()
        n_molecules = len(molecules)

        # And the molecule each atom is in
        atom_to_molecule = {}
        for molecule, atoms in enumerate(molecules):
            for atom in atoms:
                atom_to_molecule[atom] = molecule

        # The bonds in each molecule
        bonds_per_molecule = [[] for i in range(n_molecules)]
        for bond in self.bonds.bonds():
            i = bond['i']
            j = bond['j']
            order = bond['bondorder']
            molecule = atom_to_molecule[i]
            bonds_per_molecule[molecule].append((i, j, order))

        # Get the canonical smiles for each molecule
        to_can = openbabel.OBConversion()
        to_can.SetOutFormat('can')
        ob_mol = openbabel.OBMol()
        ob_template = openbabel.OBMol()
        atnos = self.atoms.atomic_numbers
        xyzs = self.atoms.coordinates

        start = 0
        new_subsets = {}
        sids = {}
        new_templates = []
        tids = []
        for molecule, atoms in enumerate(molecules):
            to_index = {j: i for i, j in enumerate(atoms)}
            n_atoms = len(atoms)
            # This is not right ... works only if atoms contiguous. Ufff.
            molecule_atnos = atnos[start:start + n_atoms]

            ob_mol.Clear()
            for atom, atno in zip(atoms, molecule_atnos):
                ob_atom = ob_mol.NewAtom()
                ob_atom.SetAtomicNum(atno)
            bonds = []
            for i, j, order in bonds_per_molecule[molecule]:
                bonds.append((to_index[i], to_index[j], order))
                # 1-based indices in ob.
                ob_mol.AddBond(to_index[i] + 1, to_index[j] + 1, order)

            canonical = to_can.WriteString(ob_mol).strip()

            if full_templates:
                # See if a molecule template with the canonical smiles exists
                if templates.exists(canonical, 'molecule'):
                    template = templates.get(canonical, category='molecule')
                else:
                    # Create a new system & configuration for the template
                    system_name = 'template system ' + canonical
                    if not self.system_db.system_exists(system_name):
                        system = self.system_db.create_system(system_name)
                        configuration = system.create_configuration(canonical)
                        cid = configuration.id

                        kwargs = {}
                        kwargs['atno'] = molecule_atnos
                        molecule_xyzs = xyzs[start:start + n_atoms]
                        kwargs['x'] = [x for x, y, z in molecule_xyzs]
                        kwargs['y'] = [y for x, y, z in molecule_xyzs]
                        kwargs['z'] = [z for x, y, z in molecule_xyzs]

                        ids = configuration.atoms.append(**kwargs)

                        kwargs = {}
                        kwargs['i'] = [ids[x] for x, _, _ in bonds]
                        kwargs['j'] = [ids[x] for _, x, _ in bonds]
                        kwargs['bondorder'] = [x for _, _, x in bonds]

                        configuration.bonds.append(**kwargs)

                        template = templates.create(
                            canonical, category='molecule', configuration=cid
                        )
            else:
                if templates.exists(canonical, 'molecule'):
                    template = templates.get(canonical, category='molecule')
                else:
                    template = templates.create(canonical, category='molecule')

            if template.id not in tids:
                tids.append(template.id)
                new_templates.append(template)

            if create_subsets:
                if full_templates:
                    # Need to reorder the atoms to match the template atoms
                    # Prepare the OB molecule for the template
                    ob_template.Clear()
                    for atno in template.atoms.atomic_numbers:
                        ob_atom = ob_template.NewAtom()
                        ob_atom.SetAtomicNum(atno)

                    tatom_ids = template.atoms.ids
                    to_index = {j: i for i, j in enumerate(tatom_ids)}
                    for row in template.bonds.bonds():
                        i = to_index[row['i']]
                        j = to_index[row['j']]
                        order = row['bondorder']
                        ob_template.AddBond(i + 1, j + 1, order)

                    # Get the mapping from template to molecule
                    query = openbabel.CompileMoleculeQuery(ob_template)
                    mapper = openbabel.OBIsomorphismMapper.GetInstance(query)
                    mapping = openbabel.vpairUIntUInt()
                    mapper.MapFirst(ob_mol, mapping)
                    reordered_atoms = [atoms[j] for i, j in mapping]

                    subset = self.subsets.create(
                        template, reordered_atoms, tatom_ids
                    )
                else:
                    subset = self.subsets.create(template, atoms)

                tid = template.id
                if tid not in sids:
                    sids[tid] = []
                    new_subsets[tid] = []
                sids[tid].append(subset.id)
                new_subsets[tid].append(subset)

            start += n_atoms

        if create_subsets:
            return new_templates, new_subsets
        else:
            return new_templates
