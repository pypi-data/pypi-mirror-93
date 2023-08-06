import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from ..constants import xyz_dict, xyz_list

def _eps_cmap(eps_r, alpha=1, cmap=None, clim=None):
    if cmap==None:
        cmap = 'Greys'
    cm = mpl.cm.get_cmap(cmap, 256)
    newmap = cm(np.linspace(0, 1, 256))
    newmap[:, 3] = alpha
    newmap[0, 3] = 0

    if clim is None:
        clim = (1, np.amax(eps_r)+1e-6)

    bounds = np.hstack((-4e6, -2e6, 0, np.linspace(clim[0], clim[1], 256)))
    eps_cmap = np.vstack(([0, 0, 1, 1], [1, 0, 0, 1], [1, 1, 1, 0], newmap))
    norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=259)

    return mpl.colors.ListedColormap(eps_cmap), norm, bounds

def _get_inside(objects, mesh):
    """ Get a mask defining points inside a list of objects.

    Parameters
    ----------
    objects : list of Structure, Source, or Monitor objects
    mesh : tuple of 3 1D arrays, or None
    
    Returns
    -------
    mask : np.ndarray
        Array of size (mesh[0].size, mesh[1].size, mesh[2].size) where each 
        element is one if inside any of the objects, and zero otherwise. 
    """

    Nx, Ny, Nz = [mesh[i].size for i in range(3)]

    mask = np.zeros((Nx, Ny, Nz))

    for obj in objects:
        mtmp = obj._inside(mesh)
        mask[mtmp > 0] = 1

    return mask

def _plot_eps(eps_r, cmap=None, clim=None, ax=None, extent=None, 
                cbar=False, cax=None, alpha=1):

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    cmplot, norm, bounds = _eps_cmap(eps_r, alpha, cmap, clim)

    im = ax.imshow(eps_r, interpolation='none', 
                norm=norm, cmap=cmplot, origin='lower', extent=extent)

    if cbar:
        if cax is not None:
            plt.colorbar(im, ax=ax, cax=cax, boundaries=bounds[3:])
        else:
            plt.colorbar(im, ax=ax, boundaries=bounds[3:])
        
    return im

def viz_eps_2D(self, normal='x', position=0., ax=None, cbar=False, clim=None,
                source_alpha=0.3, monitor_alpha=0.3, pml_alpha=0.2):
    """Plot the relative permittivity distribution of a 2D cross-section of 
    the simulation.
    
    Parameters
    ----------
    normal : {'x', 'y', 'z'}
        Axis normal to the cross-section plane.
    position : float, optional
        Position offset along the normal axis.
    ax : Matplotlib axis object, optional
        If ``None``, a new figure is created.
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    source_alpha : float, optional
        If larger than zero, overlay all sources in the simulation, 
        with transparency defined by ``source_alpha``.
    monitor_alpha : float, optional
        If larger than zero, overlay all monitors in the simulation, 
        with transparency defined by ``monitor_alpha``.
    pml_alpha : float, optional
        If larger than zero, overlay the PML boundaries of the simulation, 
        with transparency defined by ``pml_alpha``.
    
    Returns
    -------
    Matplotlib image object

    Note
    ----
    The plotting is discretized at the center positions of the Yee grid and 
    is for illustrative purposes only. In the FDTD computation, the exact 
    Yee grid is used and the permittivity values depend on the field 
    polarization.
    """

    grid = self.grid

    if ax is None:
        fig, ax = plt.subplots(1, constrained_layout=True)

    # Get normal and cross-section axes indexes
    norm = xyz_dict[normal]
    cross = [0, 1, 2]
    cross.pop(norm)

    # Get centered mesh for permittivity discretization
    mesh = [[], [], []]
    ind = np.nonzero(position < grid.mesh[norm])[0]
    if ind.size==0:
        raise ValueError("Plane position outside of simulation domain.")
    else:
        ind = ind[0]
    mesh[norm] = np.array([grid.mesh[norm][ind]])
    mesh[cross[0]] = grid.mesh[cross[0]]
    mesh[cross[1]] = grid.mesh[cross[1]]

    eps_r = np.squeeze(self._get_eps(mesh))

    # Get mesh for source and monitor discretization
    if ind > 0:
        mesh_sp = [[], [], []]
        mesh_sp[norm] = grid.mesh[norm][ind-1:ind+1]
        mesh_sp[cross[0]] = mesh[cross[0]]
        mesh_sp[cross[1]] = mesh[cross[1]]

    # Plot and set axes properties
    extent = [grid.mesh[cross[0]][0], grid.mesh[cross[0]][-1], 
                    grid.mesh[cross[1]][0], grid.mesh[cross[1]][-1]]
    x_lab = xyz_list[cross[0]]
    y_lab = xyz_list[cross[1]]
    ax_tit = x_lab+y_lab + "-plane at " + xyz_list[norm] + "=%1.2f" % position
    npml = self.Npml[[cross[0], cross[1]], :]

    im = _plot_eps(eps_r.T, clim=clim, ax=ax, extent=extent, cbar=cbar)
    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.set_title(ax_tit)

    def squeeze_mask(mask, axis):
        inds = [slice(None), slice(None), slice(None)]
        inds[axis] = 1
        return np.squeeze(mask[tuple(inds)])

    if monitor_alpha > 0:
        monitor_alpha = min(monitor_alpha, 1)
        mnt_mask = squeeze_mask(_get_inside(self.monitors, mesh=mesh_sp), norm)
        mnt_cmap = mpl.colors.ListedColormap(np.array([[0, 0, 0, 0],
                            [236/255, 203/255, 32/255, monitor_alpha]]))
        ax.imshow(mnt_mask.T, clim=(0, 1), cmap=mnt_cmap, origin='lower',
                        extent=extent)

    if source_alpha > 0:
        source_alpha = min(source_alpha, 1)
        src_mask = squeeze_mask(_get_inside(self.sources, mesh=mesh_sp), norm)
        src_cmap = mpl.colors.ListedColormap(np.array([[0, 0, 0, 0],
                            [78/255, 145/255, 78/255, source_alpha]]))
        ax.imshow(src_mask.T, clim=(0, 1), cmap=src_cmap, origin='lower',
                        extent=extent)

    if pml_alpha >0 :
        pml_alpha = min(pml_alpha, 1)
        pml_mask = np.squeeze(np.zeros((mesh[0].size, mesh[1].size,
                                                mesh[2].size)))
        N1, N2 = pml_mask.shape
        pml_mask[:npml[0, 0], :] = 1
        pml_mask[N1-npml[0, 1]:, :] = 1
        pml_mask[:, :npml[1, 0]] = 1
        pml_mask[:, N2-npml[1, 1]:] = 1
        pml_cmap = mpl.colors.ListedColormap(np.array([[0, 0, 0, 0],
                            [229/255, 127/255, 25/255, pml_alpha]]))
        ax.imshow(pml_mask.T, clim=(0, 1), cmap=pml_cmap, origin='lower',
                        extent=extent)

    return im