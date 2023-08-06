import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from ..utils import listify
from .field import _plot_field_2D

def _mode_plane(mode_plane, freq_ind=0, mode_inds=0,
                val='abs', cbar=False, eps=True, clim=None):

    minds = listify(mode_inds)
    grid_list = [(1, 2, 0, 'y', 'z'),
                (0, 2, 1, 'x', 'z'),
                (0, 1, 2, 'x', 'y')]

    (d1, d2, dn, x_lab, y_lab) = grid_list[mode_plane.norm_ind]
    N1, N2 = mode_plane.eps.shape

    if eps==True:
        eps_r = mode_plane.eps
    else:
        eps_r = None

    mesh_c1 = mode_plane.mesh[0]
    mesh_c2 = mode_plane.mesh[1]
    extent = [mesh_c1[0], mesh_c1[-1], mesh_c2[0], mesh_c2[-1]]
    aspect = (extent[3]-extent[2])/(extent[1]-extent[0])

    fig, axs = plt.subplots(len(minds), 2, figsize=(8, 4*aspect*len(minds)),
                            constrained_layout=True)
    if len(minds)==1:
        axs = axs.reshape((1, 2))

    for iax, imode in enumerate(minds):
        (E, _) = mode_plane.modes[freq_ind][imode].fields_to_center()
        Ec1 = E[0, :, :]
        Ec2 = E[1, :, :]

        _clim = clim
        if clim is None:
            cmax = np.amax(np.abs(np.vstack((Ec1, Ec2))))
            if val=='abs':
                _clim = (0, cmax)
            else:
                _clim = (-cmax, cmax)

        subtitle = "f=%1.2eTHz, "%(mode_plane.freqs[freq_ind]*1e-12)
        subtitle += "n=%1.2f"%mode_plane.modes[freq_ind][imode].neff
        ax_title = "Mode %d, E%s"%(imode, x_lab) + "\n" + subtitle
        _plot_field_2D(Ec1, eps_r, extent, x_lab, y_lab, ax_title,
                        val=val, ax=axs[iax, 0], cbar=False, clim=_clim)
        ax_title = "Mode %d, E%s"%(imode, y_lab) + "\n" + subtitle
        _plot_field_2D(Ec2, eps_r, extent, x_lab, y_lab, ax_title,
                        val=val, ax=axs[iax, 1], cbar=cbar, clim=_clim)

    return fig

def viz_modes(self, obj, freq_ind=0, mode_inds=0,
                val='abs', cbar=False, clim=None, eps_alpha=0.3):
    """Plot the field distribution of (a subset of) the 2D eigenmodes of 
    a :class:`.ModeSource` or a `:class:`.ModeMonitor`.
    
    Parameters
    ----------
    obj : ModeSource or ModeMonitor
        Generally, object that has a ``mode_plane`` attribute.
    freq_ind : int, optional
        Frequency index of the stored modes to be plotted.
    mode_inds : array_like, optional
        Mode indexes of the stored modes to be plotted.
    val : {'re', 'im', 'abs'}, optional
        Plot the real part (default), or the imaginary or absolute value of 
        the field components.
    cbar : bool, optional
        Add a colorbar to the plot.
    clim : List[float], optional
        Matplotlib color limit to use for plot.
    eps_alpha : float, optional
        If larger than zero, overlay the underlying permittivity distribution, 
        with transparency defined by eps_alpha.

    Returns
    -------
    Matplotlib figure object

    Note
    ----
    If the modes have not been computed yet, or ``mode_inds`` exceeds the 
    largest mode index that is stored in ``obj``, the eigenmode computation 
    will be called.
    """
    mode_pl = obj.mode_plane
    nfreqs = len(mode_pl.modes)

    # Check if frequency index out of bounds
    if nfreqs < freq_ind:
        raise ValueError("Frequency index %d our of bounds for "%freq_ind + 
                        "ModePlane number of frequencies %d."%nfreqs)

    # Check if modes have not been computed yet, or if fewer than requested
    if len(mode_pl.modes[freq_ind]) <= np.amax(mode_inds):
        mode_pl.get_modes(np.amax(mode_inds) + 1, mode_pl.freqs)

    _mode_plane(mode_pl, freq_ind, mode_inds,
                val=val, cbar=cbar, clim=clim, eps_alpha=eps_alpha)

    return fig