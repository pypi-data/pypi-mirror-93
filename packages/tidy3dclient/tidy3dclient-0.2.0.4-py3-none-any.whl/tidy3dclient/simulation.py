import numpy as np
import json
import h5py

from .utils import listify, cs2span, intersect_box, check_3D_lists, object_name
from .constants import int_, float_, fp_eps, C_0
from .structure import Structure, Box
from .source import Source, ModeSource, SourceData
from .monitor import (Monitor, TimeMonitor, FreqMonitor, ModeMonitor,
                        MonitorData)
from .grid import Grid
from .material import Medium
from . import PEC, PMC
from .json_ops import (write_parameters, write_structures, write_sources,
                        write_monitors)
from . import viz

class Simulation(object):
    """
    Main class for building a simulation model.
    """

    from .monitor._simulation import (data, poynting, flux, decompose, 
                                        _compute_modes_monitor)
    from .source._simulation import _compute_modes_source, set_mode, spectrum
    from .viz import (_fmonitors_png, viz_eps_2D, viz_field_2D, viz_modes,
                        viz_source, viz_source_spectrum, viz_source_time)
    from .json_ops import _read_simulation

    def __init__(self,
                size,
                center=[0., 0., 0.],
                resolution=None,
                mesh_step=None,
                structures=None,
                sources=None,
                monitors=None,
                symmetries=[0, 0, 0],
                pml_layers=[0, 0, 0],
                run_time=0.,
                courant=0.9,
                verbose=True
                ):
        """Construct.

        Parameters
        ----------
        center : array_like, optional
            (micron) 3D vector defining the center of the simulation domain.
        size : array_like, optional
            (micron) 3D vector defining the size of the simulation domain.
        resolution : float or array_like, optional
            (1/micron) Number of pixels per micron, or a 3D vector defining 
            the number of pixels per mircon in x, y, and z seprately.
        mesh_step : float or array_like, optional
            (micron) Step size in all directions, or a 3D vector defining the 
            step size in x, y, and z seprately. If provided, ``mesh_step`` 
            overrides the ``resolution`` parameter, otherwise 
            ``mesh_step = 1/resolution``.
        structures : Structure or List[Structure], optional
            Empty list (default) means vacuum. 
        sources : Source or List[Source], optional
            Source(s) to be added to the simulation.
        monitors : Monitor or List[Monitor], optional
            Monitor(s) to be added to the simulation.
        symmetries : array_like, optional
            Array of three integers defining reflection symmetry across a 
            plane bisecting the simulation domain normal to the x-, y-, and 
            z-axis, respectively. Each element can be ``0`` (no symmetry), 
            ``1`` (even, i.e. 'PMC' symmetry) or ``-1`` (odd, i.e. 'PEC' 
            symmetry). Note that the vectorial nature of the fields must be 
            taken into account to correctly determine the symmetry value.
        pml_layers : array_like, optional
            Array of three integers defining the number of PML layers on both 
            sides of the simulation domain along x, y, and z. When set to 
            ``0`` (default), periodic boundary conditions are applied.
        run_time : float, optional
            (second) Total electromagnetic evolution time.
        courant : float, optional
            Courant stability factor, must be smaller than 1, or more 
            generally smaller than the smallest refractive index in the 
            simulation.
        verbose : bool, optional
            Print helpful messages regarding the simulation.
        """

        check_3D_lists(center=listify(center), size=listify(size),
                            symmetries=listify(symmetries),
                            pml_layers=listify(pml_layers))

        self.verbose = verbose
        self._print("Initializing simulation...")

        self.center = np.array(center, dtype=float_)
        self.size = np.array(size, dtype=float_)
        self.span = cs2span(self.center, self.size)

        # Space and time grid
        if mesh_step is None:
            if resolution is None:
                raise ValueError("Either 'mesh_step' or 'resolution' must be "
                                "set.")
            mesh_step = 1/np.array(resolution)
        else:
            if resolution is not None:
                self._print("Note: parameter 'mesh_step' overrides "
                            "'resolution'.")
        self.grid = Grid(self.span, mesh_step, symmetries, courant)
        self._print("Simulation domain in number of pixels: "
                    "%d, %d, %d."%(self.grid.Nxyz[0], self.grid.Nxyz[1], 
                                    self.grid.Nxyz[2]))

        # Computational domain including symmetries, if any
        self.span_sym = np.copy(self.span)
        self.Nxyz_sym = np.copy(self.grid.Nxyz)
        for d, sym in enumerate(symmetries):
            if sym==-1:
                self.span_sym[d, 0] += self.size[d]/2
                self.Nxyz_sym[d] = self.Nxyz_sym[d]//2
            elif sym==1:
                self.span_sym[d, 0] += self.size[d]/2 - self.grid.res[d]
                self.span_sym[d, 1] += self.grid.res[d]
                self.Nxyz_sym[d] = self.Nxyz_sym[d]//2 + 2
        # Print new size, if there are any symmetries
        if np.any(np.array(symmetries)!=0):
            self._print("Computation domain (after symmetries): "
                    "%d, %d, %d."%(self.Nxyz_sym[0], self.Nxyz_sym[1], 
                                    self.Nxyz_sym[2]))

        # Print resolution, set and print run time
        self._print("Mesh step (micron): %1.2e, %1.2e, %1.2e."%(
                        self.grid.res[0], self.grid.res[1], self.grid.res[2]))
        self._set_run_time(run_time)
        self.courant = courant
        self._print("Total number of time steps: %d."%(self.Nt))
        self._check_size()

        # Set PML size and compute parameters
        self.pml_layers = listify(pml_layers)
        self.Npml = np.vstack((pml_layers, pml_layers)).astype(int_).T

        # Materials and indexing populated when adding ``Structure`` objects.
        self._mat_inds = [] # material index of each structure
        self._materials = [] # list of materials included in the simulation
        self._structures = []

        # List containing SourceData for all sources, and a dictionary 
        # used to get SourceData from id(source), e.g. src_data = 
        # self._source_ids[id(source)]
        self._source_data = []
        self._source_ids = {}

        # List containing MonitorData for all monitors, and a dictionary 
        # used to get MonitorData from id(monitor)
        self._monitor_data = []
        self._monitor_ids = {}

        # Structures and material indexing for symmetry boxes
        self._structures_sym = [] # PEC/PMC boxes added for symmetry
        self._mat_inds_sym = []

        # Add structures, sources, monitors, symmetries
        if structures:
            self.add(structures)
        if sources:
            self.add(sources)
        if monitors:
            self.add(monitors)
        self._add_symmetries(symmetries)

        # JSON file from which the simulation is loaded
        self.fjson = None

    def __repr__(self):
        rep = "Tidy3D Simulation:\n"
        rep += "center     = [" + ' '.join(["%1.4f"%c 
                                    for c in self.center]) + "] \n"
        rep += "size       = [" + ' '.join(["%1.4f"%s 
                                    for s in self.size]) + "] \n"
        rep += "mesh_step  = [" + ' '.join(["%1.4f"%r
                                    for r in self.grid.res]) + "] \n"
        rep += "run_time   = %1.2e\n"%self.run_time
        rep += "symmetries = [" + ' '.join(["%d"%s 
                                    for s in self.symmetries]) + "] \n"
        rep += "pml_layers = [" + ' '.join(["%d"%p
                                    for p in self.pml_layers]) + "] \n\n"

        rep += "Number of time points      : %d\n"%self.Nt
        rep += "Number of pixels in x, y, z: %d, %d, %d\n"%(self.grid.Nx,
                                            self.grid.Ny, self.grid.Nz)
        rep += "Number of pixels including \n" +\
               "symmetries                 : %d, %d, %d\n"%(self.Nxyz_sym[0],
                                            self.Nxyz_sym[1], self.Nxyz_sym[2])
        rep += "Number of strictures       : %d\n"%len(self._structures)
        rep += "Number of sources          : %d\n"%len(self.sources)
        rep += "Number of monitors         : %d\n"%len(self.monitors)

        return rep

    @property
    def materials(self):
        """ List conaining all materials included in the simulation."""
        return self._materials

    @property
    def mat_inds(self):
        """ List conaining the material index in :attr:`.materials` of every 
        structure in :attr:`.structures`. """
        return self._mat_inds + self._mat_inds_sym

    @property
    def structures(self):
        """ List conaining all :class:`Structure` objects. """
        return self._structures + self._structures_sym

    @structures.setter
    def structures(self, new_struct):
        raise RuntimeError("Structures can be added upon Simulation init, "
                            "or using 'Simulation.add()'")

    @property
    def sources(self):
        """ List conaining all :class:`Source` objects. """
        return [src_data.source for src_data in self._source_data]

    @sources.setter
    def sources(self, new_sources):
        raise RuntimeError("Sources can be added upon Simulation init, "
                            "or using 'Simulation.add()'")

    @property
    def monitors(self):
        """ List conaining all :class:`.Monitor` objects. """
        return [mnt_data.monitor for mnt_data in self._monitor_data]

    @monitors.setter
    def monitors(self, new_monitors):
        raise RuntimeError("Monitors can be added upon Simulation init, "
                            "or using 'Simulation.add()'")

    def _print(self, message):
        if self.verbose==True:
            print(message)

    def _check_size(self):
        Np = np.prod(self.Nxyz_sym)
        if self.Nt > 1e8:
            raise RuntimeError("Time steps %1.2e exceed current limit 1e8, "
                "reduce 'run_time' or increase the spatial mesh step."%self.Nt)

        if Np > 2e9:
            raise RuntimeError("Total number of grid points %1.2e exceeds "
                "current limit 2e9, increase the mesh step or decrease the "
                "size of the simulation domain."%Np)

        if Np*self.Nt > 2e14:
            raise RuntimeError("Product of grid points and time steps "
                "%1.2e exceeds current limit 2e14. Increase the mesh step or "
                "decrease the 'run_time' of the simulation."%Np*self.Nt)

    def _add_structure(self, structure):
        """ Adds a Structure object to the list of structures and to the 
        permittivity array. """
        self._structures.append(structure)

        try:
            mind = self.materials.index(structure.material)
            self._mat_inds.append(mind)
        except ValueError:
            if len(self.materials) < 200:
                self._materials.append(structure.material)
                self._mat_inds.append(len(self.materials)-1)
            else:
                raise RuntimeError("Maximum 200 distinct materials allowed.")

    def _add_source(self, source):
        """ Adds a Source object to the list of sources.
        """

        if id(source) in self._monitor_ids.keys():
            print("Source already in Simulation.")
            return

        src_data = SourceData(source)
        src_data.name = object_name(self._source_data, source, 'source')
        src_data._mesh_norm(self.grid.res)
        src_data._set_tdep(self.grid.tmesh)
        self._source_data.append(src_data)
        self._source_ids[id(source)] = src_data

        if isinstance(source, ModeSource):
            src_data.mode_plane._set_eps(self)

    def _add_monitor(self, monitor):
        """ Adds a time or frequency domain Monitor object to the 
        corresponding list of monitors.
        """

        if id(monitor) in self._monitor_ids.keys():
            print("Monitor already in Simulation.")
            return

        mnt_data = MonitorData(monitor)
        mnt_data.name = object_name(self._monitor_data, monitor, 'monitor')
        self._monitor_data.append(mnt_data)
        self._monitor_ids[id(monitor)] = mnt_data

        # Compute how many grid points there are inside the monitor
        span_in = intersect_box(self.span_sym, monitor.span)
        size_in = span_in[:, 1] - span_in[:, 0]
        if np.any(size_in < 0):
            Np = 0
        else:
            Np = np.prod([int(s)/self.grid.res[d] + 1 
                    for (d, s) in enumerate(size_in)])

        if isinstance(monitor, TimeMonitor):
            mnt_data._set_tmesh(self.grid.tmesh)
            # 4 bytes x N points x N time steps x 3 components x N fields
            memGB = 4*Np*mnt_data.Nt*3*len(monitor.field)/1e9
            if memGB > 10:
                raise RuntimeError("Estimated time monitor size %1.2f GB "
                "exceeds current limit of 10GB per monitor. Decrease monitor "
                "size or the time interval using 't_start' and 't_stop'."
                %memGB)

        elif isinstance(monitor, FreqMonitor):
            # 8 bytes x N points x N freqs x 3 components x N fields
            memGB = 8*Np*len(mnt_data.freqs)*3*len(monitor.field)/1e9
            if memGB > 10:
                raise RuntimeError("Estimated frequency monitor size %1.2f GB "
                "exceeds current limit of 10GB per monitor. Decrease monitor "
                "size or the number of frequencies."%memGB)

        self._print("Estimated data size of monitor "
                    "%s: %1.4fGB."%(mnt_data.name, memGB))

        # Initialize the ModePlane of a ModeMonitor
        if isinstance(monitor, ModeMonitor):
            mnt_data._set_mode_plane()
            mnt_data.mode_plane._set_eps(self)

    def _add_symmetries(self, symmetries):
        """ Add all symmetries as PEC or PMC boxes.
        """
        self.symmetries = listify(symmetries)
        for dim, sym in enumerate(symmetries):
            if sym not in [0, -1, 1]:
                raise ValueError ("Reflection symmetry values can be 0 (no "
                                "symmetry), 1, or -1.")
            elif sym==1 or sym==-1:
                sym_cent = np.copy(self.center)
                sym_size = np.copy(self.size)
                sym_cent[dim] -= self.size[dim]/2
                sym_size[dim] = sym_size[dim] + fp_eps
                sym_mat = PEC if sym==-1 else PMC
                sym_pre = 'pec' if sym==-1 else 'pmc'
                self._structures_sym.append(Box(center=sym_cent,
                                                size=sym_size,
                                                material=sym_mat,
                                                name=sym_pre + '_sym%d'%dim))
                try:
                    mind = self.materials.index(sym_mat)
                    self._mat_inds_sym.append(mind)
                except ValueError:
                    self._materials.append(sym_mat)
                    self._mat_inds_sym.append(len(self.materials)-1)

    def _pml_config(self):
        """Set the CPML parameters. Default configuration is hard-coded. This 
        could eventually be exposed to the user, or, better, named PML 
        profiles can be created.
        """
        cfs_config = {'sorder': 3, 'smin': 0., 'smax': None, 
                    'korder': 3, 'kmin': 1., 'kmax': 3., 
                    'aorder': 1, 'amin': 0., 'amax': 0}
        return cfs_config

    def _set_run_time(self, run_time):
        """ Set the total time (in seconds) of the simulated field evolution.
        """
        self.run_time = run_time
        self.grid.set_tmesh(self.run_time)
        self.Nt = np.int(self.grid.tmesh.size)

    def _get_eps(self, mesh, edges='in', pec_val=-1e6, pmc_val=-3e6):
        """ Compute the permittivity over a given mesh. For large simulations, 
        this could be computationally heavy, so preferably use only over small 
        meshes (e.g. 2D cuts). 
        
        Parameters
        ----------
        mesh : tuple
            Three 1D arrays defining the mesh in x, y, z.
        edges : {'in', 'out', 'average'}
            When an edge of a structure sits exactly on a mesh point, it is 
            counted as in, out, or an average value of in and out is taken.
        pec_val : float
            Value to use for PEC material.
        pmc_val : float
            Value to use for PMC material.
        
        Returns
        -------
        eps : np.ndarray
            Array of size (mesh[0].size, mesh[1].size, mesh[2].size) defining 
            the relative permittivity at each point.
        """

        Nx, Ny, Nz = [mesh[i].size for i in range(3)]

        eps = np.ones((Nx, Ny, Nz), dtype=float_)

        # Apply all structures
        for struct in self.structures:

            eps_val = struct._get_eps_val(pec_val, pmc_val)
            struct._set_val(mesh, eps, eps_val, edges=edges)

        # return eps array after filling in all structures
        return eps

    def add(self, objects):
        """Add a list of objects, which can contain structures, sources, and 
        monitors.
        """

        for obj in listify(objects):
            if isinstance(obj, Structure):
                self._add_structure(obj)
            elif isinstance(obj, Source):
                self._add_source(obj)
            elif isinstance(obj, Monitor):
                self._add_monitor(obj)

    def load_results(self, dfile):
        """Load all monitor data recorded from a Tidy3D run.
        The data from each monitor can then be queried using 
        :meth:`.data`.
        
        Parameters
        ----------
        dfile : str
            Path to the file containing the simulation results.
        """

        mfile = h5py.File(dfile, "r")
        for (im, mnt_data) in enumerate(self._monitor_data):
            mname = mnt_data.name
            mnt_data._load_fields(mfile[mname]["indspan"][0, :],
                            mfile[mname]["indspan"][1, :],
                            np.array(mfile[mname]["E"]),
                            np.array(mfile[mname]["H"]), 
                            self.symmetries, self.grid.Nxyz)
            mnt_data.xmesh = np.array(mfile[mname]["xmesh"])
            mnt_data.ymesh = np.array(mfile[mname]["ymesh"])
            mnt_data.zmesh = np.array(mfile[mname]["zmesh"])
            mnt_data.mesh_step = self.grid.res

        mfile.close()
        fmonitors = [mnt for mnt in self.monitors
                            if isinstance(mnt, FreqMonitor)]
        if len(fmonitors) > 0:
            if len(self.sources) > 0: 
                self.source_norm(self.sources[0])
                self._print("Applying source normalization to all frequency "
                        "monitors using source index 0.\nTo revert, "
                        "use Simulation.source_norm(None).")
                if len(self.sources) > 1:
                    self._print("To select a different "
                        "source for the normalization: "
                        "Simulation.source_norm(source).")
                        

    def source_norm(self, source):
        """Normalize all frequency monitors by the spectrum of a 
        :class:`.Source` object.
        
        Parameters
        ----------
        source : Source or None
            If ``None``, the normalization is reset to the raw field output.
        """

        if source is None:
            for mnt_data in self._monitor_data:
                mnt_data.set_source_norm(None)
            return

        src_data = self._source_ids[id(source)]

        for mnt_data in self._monitor_data:
            mnt_data.set_source_norm(src_data)

    def compute_modes(self, mode_object, Nmodes):
        """Compute the eigenmodes of the 2D cross-section of a 
        :class:`.ModeSource` or :class:`.ModeMonitor` object, assuming 
        translational invariance in the third dimension. The eigenmodes are 
        computed in decreasing order of propagation constant, at the central 
        frequency of the :class:`.ModeSource` or for every frequency in the 
        list of frequencies of the :class:`.ModeMonitor`. In-plane, periodic 
        boundary conditions are assumed, such that the mode shold decay at the 
        boundaries, or be matched with periodic boundary conditions in the 
        simulation. Use :meth:`.viz_modes` to visuzlize the computed 
        eigenmodes.
        
        Parameters
        ----------
        mode_object : ModeSource or ModeMonitor
            The object defining the 2D plane in which to compute the modes.
        Nmodes : int
            Number of eigenmodes to compute.
        """

        if isinstance(mode_object, Monitor):
            self._compute_modes_monitor(mode_object, Nmodes)
        elif isinstance(mode_object, Source):
            self._compute_modes_source(mode_object, Nmodes)

    def export(self):
        """Return a dictionary with all simulation parameters and objects.
        """
        js = {}
        js["parameters"] = write_parameters(self)
        js["sources"] = write_sources(self)
        js["monitors"] = write_monitors(self)
        js["materials"], js["structures"] = write_structures(self)

        return js

    def export_json(self, fjson):
        """Export the simulation dictionary to a JSON file.
        
        Parameters
        ----------
        fjson : str
            JSON file name.
        """

        self.fjson = fjson
        with open(fjson, 'w') as json_file:
            json.dump(self.export(), json_file, indent=4)

    @classmethod
    def import_json(cls, fjson):
        """Import a simulation from a JSON file.
        
        Parameters
        ----------
        fjson : str
            JSON file name.
        """
        
        with open(fjson, 'r') as json_file:
            js = json.load(json_file)

        sim = cls._read_simulation(js)
        sim.fjson = fjson

        return sim