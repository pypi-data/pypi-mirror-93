import math
from .material import Medium
from .dispersion import DispersionModel, Sellmeier, Lorentz
from .constants import C_0, HBAR


class cSi(Medium):
    """Crystalline silicon at 26 deg C.

    Refs:
    * A. Deinega, I. Valuev, B. Potapkin, and Y. Lozovik, Minimizing light
      reflection from dielectric textured surfaces,
      J. Optical Society of America A, 28, 770-77 (2011).
    * M. A. Green and M. Keevers, Optical properties of intrinsic silicon
      at 300 K, Progress in Photovoltaics, 3, 189-92 (1995).
    * C. D. Salzberg and J. J. Villa. Infrared Refractive Indexes of Silicon,
      Germanium and Modified Selenium Glass,
      J. Opt. Soc. Am., 47, 244-246 (1957).
    * B. Tatian. Fitting refractive-index data with the Sellmeier dispersion
      formula, Appl. Opt. 23, 4477-4485 (1984).
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        if variant is None:
            variant = "Deinega2011"

        if "SalzbergVilla1957" == variant:
            self.dispmod = Sellmeier(
                [
                    (10.6684293, 0.301516485 ** 2),
                    (0.0030434748, 1.13475115 ** 2),
                    (1.54133408, 1104 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 11.00, C_0 / 1.36)
        elif "Deinega2011" == variant:
            self.dispmod = Lorentz(
                self.eps,
                [
                    (8.000, 3.64 * C_0, 0),
                    (2.850, 2.76 * C_0, 0.063 * C_0),
                    (-0.107, 1.73 * C_0, 2.5 * C_0),
                ],
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.0, C_0 / 0.4)


class aSi(Medium):
    """Amorphous silicon

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 3.109
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(17.68 - self.eps, 3.93 * eV_to_Hz, 1.92 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6 * eV_to_Hz)


class AlAs(Medium):
    """AlAs

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(8.27 - self.eps, 4.519 * eV_to_Hz, 0.378 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0 * eV_to_Hz, 3 * eV_to_Hz)


class AlGaN(Medium):
    """AlGaN

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(4.6 - self.eps, 7.22 * eV_to_Hz, 0.127 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 4 * eV_to_Hz)


class AlN(Medium):
    """AlN

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(4.306 - self.eps, 8.916 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4.75 * eV_to_Hz)


class Al2O3(Medium):
    """Alumina

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.52 - self.eps, 12.218 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 6 * eV_to_Hz)


class AlxOy(Medium):
    """AlxOy

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.171 - self.eps, 12.866 * eV_to_Hz, 0.861 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 6 * eV_to_Hz)


class Aminoacid(Medium):
    """Amino acid

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(1.486 - self.eps, 14.822 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5 * eV_to_Hz)


class CaF2(Medium):
    """CaF2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.036 - self.eps, 15.64 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4.75 * eV_to_Hz)


class GeOx(Medium):
    """GeOx

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.645 - self.eps, 16.224 * eV_to_Hz, 0.463 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 4 * eV_to_Hz)


class H2O(Medium):
    """Water

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(1.687 - self.eps, 11.38 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6 * eV_to_Hz)


class HfO2(Medium):
    """HfO2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.9 - self.eps, 9.4 * eV_to_Hz, 3.0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6 * eV_to_Hz)


class HMDS(Medium):
    """HMDS

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.1 - self.eps, 12.0 * eV_to_Hz, 0.5 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6.5 * eV_to_Hz)


class ITO(Medium):
    """Indium Tin Oxide

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.5 - self.eps, 6.8 * eV_to_Hz, 0.637 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6 * eV_to_Hz)


class MgF2(Medium):
    """MgF2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(1.899 - self.eps, 16.691 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.8 * eV_to_Hz, 3.8 * eV_to_Hz)


class MgO(Medium):
    """MgO

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 11.232
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.599 - self.eps, 1.0 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5.5 * eV_to_Hz)


class PEI(Medium):
    """PEI

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.09 - self.eps, 12.0 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4.75 * eV_to_Hz)


class PEN(Medium):
    """PEN

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.466 - self.eps, 4.595 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 3.2 * eV_to_Hz)


class PET(Medium):
    """PET

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.2 - self.eps, 7.0 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = None


class PMMA(Medium):
    """PMMA

    Refs:
    * N. Sultanova, S. Kasarova and I. Nikolov.
      Dispersion properties of optical polymers,
      Acta Physica Polonica A 116, 585-587 (2009)
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Sultanova2009"

        if "Horiba" == variant:
            eV_to_Hz = 0.5 / (math.pi * HBAR)
            self.dispmod = Lorentz(
                self.eps, [(2.17 - self.eps, 11.427 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4.55 * eV_to_Hz)
        elif "Sultanova2009" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.1819, 0.011313),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.052, C_0 / 0.4368)


class Polycarbonate(Medium):
    """Polycarbonate

    Refs:
    * N. Sultanova, S. Kasarova and I. Nikolov.
      Dispersion properties of optical polymers,
      Acta Physica Polonica A 116, 585-587 (2009)
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Sultanova2009"

        if "Horiba" == variant:
            eV_to_Hz = 0.5 / (math.pi * HBAR)
            self.dispmod = Lorentz(
                self.eps, [(2.504 - self.eps, 12.006 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 4 * eV_to_Hz)
        elif "Sultanova2009" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.4182, 0.021304),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.052, C_0 / 0.4368)


class Polystyrene(Medium):
    """Polystyrene

    Refs:
    * N. Sultanova, S. Kasarova and I. Nikolov.
      Dispersion properties of optical polymers,
      Acta Physica Polonica A 116, 585-587 (2009)
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Sultanova2009"

        if "Sultanova2009" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.4435, 0.020216),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.052, C_0 / 0.4368)


class Cellulose(Medium):
    """Cellulose

    Refs:
    * N. Sultanova, S. Kasarova and I. Nikolov.
      Dispersion properties of optical polymers,
      Acta Physica Polonica A 116, 585-587 (2009)
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Sultanova2009"

        if "Sultanova2009" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.124, 0.011087),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.052, C_0 / 0.4368)


class pSi(Medium):
    """Poly-silicon

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(12.0 - self.eps, 4.0 * eV_to_Hz, 0.5 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5 * eV_to_Hz)


class PTFE(Medium):
    """PTFE

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(1.7 - self.eps, 16.481 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6.5 * eV_to_Hz)


class PVC(Medium):
    """PVC

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.304 - self.eps, 12.211 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 4.75 * eV_to_Hz)


class Sapphire(Medium):
    """Sapphire

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.09 - self.eps, 13.259 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5.5 * eV_to_Hz)


class SiC(Medium):
    """SiC

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 3.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(6.8 - self.eps, 8.0 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 4 * eV_to_Hz)


class SiN(Medium):
    """SiN

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 2.32
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.585 - self.eps, 6.495 * eV_to_Hz, 0.398 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 6 * eV_to_Hz)


class Si3N4(Medium):
    """Si3N4

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    * H. R. Philipp. Optical properties of silicon nitride, J. Electrochim. Soc. 120, 295-300 (1973)
    * T. Baak. Silicon oxynitride; a material for GRIN optics, Appl. Optics 21, 1069-1072 (1982)
    * K. Luke, Y. Okawachi, M. R. E. Lamont, A. L. Gaeta, M. Lipson.
      Broadband mid-infrared frequency comb generation in a Si3N4 microresonator,
      Opt. Lett. 40, 4823-4826 (2015)
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(5.377 - self.eps, 3.186 * eV_to_Hz, 1.787 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5.5 * eV_to_Hz)
        elif "Philipp1973" == variant:
            self.dispmod = Sellmeier(
                [
                    (2.8939, 0.13967 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.24, C_0 / 0.207)
        elif "Luke2015" == variant:
            self.dispmod = Sellmeier(
                [
                    (3.0249, 0.1353406 ** 2),
                    (40314, 1239.842 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 5.504, C_0 / 0.31)


class SiO2(Medium):
    """SiO2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.12 - self.eps, 12.0 * eV_to_Hz, 0.1 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.7 * eV_to_Hz, 5 * eV_to_Hz)


class SiON(Medium):
    """SiON

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.342 - self.eps, 10.868 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 3 * eV_to_Hz)


class Ta2O5(Medium):
    """Ta2O5

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(4.133 - self.eps, 7.947 * eV_to_Hz, 0.814 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4 * eV_to_Hz)


class TiOx(Medium):
    """TiOx

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 0.29
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.82 - self.eps, 6.5 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 3 * eV_to_Hz)


class Y2O3(Medium):
    """Y2O3

    Refs:
    * Y. Nigara. Measurement of the optical constants of yttrium oxide,
      Jpn. J. Appl. Phys. 7, 404-408 (1968)
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Nigara1968"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.715 - self.eps, 9.093 * eV_to_Hz, 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.55 * eV_to_Hz, 4 * eV_to_Hz)
        elif "Nigara1968" == variant:
            self.dispmod = Sellmeier(
                [
                    (2.578, 0.1387 ** 2),
                    (3.935, 22.936 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 9.6, C_0 / 0.25)


class ZrO2(Medium):
    """ZrO2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.829 - self.eps, 9.523 * eV_to_Hz, 0.128 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 3 * eV_to_Hz)


class AlAs(Medium):
    """AlAs

    Refs:
    * R.E. Fern and A. Onton, J. Applied Physics, 42, 3499-500 (1971)
    """

    def __init__(self, variant=None):
        self.eps = 2.0792
        self.sigma = 0

        if variant is None:
            variant = "FernOnton1971"

        if "FernOnton1971" == variant:
            self.dispmod = Sellmeier(
                [
                    (6.0840, 0.2822 ** 2),
                    (1.900, 27.62 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 2.2, C_0 / 0.56)


class BK7(Medium):
    """N-BK7 borosilicate glass"""

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        if variant is None:
            variant = "Zemax"

        if "Zemax" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.03961212, 0.00600069867),
                    (0.231792344, 0.0200179144),
                    (1.01046945, 103.560653),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 2.5, C_0 / 0.3)


class FusedSilica(Medium):
    """Fused silica

    Refs:
    * I. H. Malitson. Interspecimen comparison of the refractive index of
      fused silica, J. Opt. Soc. Am. 55, 1205-1208 (1965)
    * C. Z. Tan. Determination of refractive index of silica glass for
      infrared wavelengths by IR spectroscopy,
      J. Non-Cryst. Solids 223, 158-163 (1998)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        if variant is None:
            variant = "Zemax"

        if "Zemax" == variant:
            self.dispmod = Sellmeier(
                [
                    (0.6961663, 0.0684043 ** 2),
                    (0.4079426, 0.1162414 ** 2),
                    (0.8974794, 9.896161 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 6.7, C_0 / 0.21)


class GaAs(Medium):
    """Gallium arsenide

    Refs:
    * T. Skauli, P. S. Kuo, K. L. Vodopyanov, T. J. Pinguet, O. Levi,
      L. A. Eyres, J. S. Harris, M. M. Fejer, B. Gerard, L. Becouarn,
      and E. Lallier. Improved dispersion relations for GaAs and
      applications to nonlinear optics, J. Appl. Phys., 94, 6447-6455 (2003)
    """

    def __init__(self, variant=None):
        self.eps = 5.372514
        self.sigma = 0

        if variant is None:
            variant = "Skauli2003"

        if "Skauli2003" == variant:
            self.dispmod = Sellmeier(
                [
                    (5.466742, 0.4431307 ** 2),
                    (0.02429960, 0.8746453 ** 2),
                    (1.957522, 36.9166 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 17, C_0 / 0.97)


class Ag(Medium):
    """Silver.

    Refs:
    * A. D. Rakic et al., Applied Optics, 37, 5271-5283 (1998)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (-2.502e-2 - 8.626e-3j, 5.987e-1 + 4.195e3j),
                    (-2.021e-1 - 9.407e-1j, -2.211e-1 + 2.680e-1j),
                    (-1.467e1 - 1.338e0j, -4.240e0 + 7.324e2j),
                    (-2.997e-1 - 4.034e0j, 6.391e-1 - 7.186e-2j),
                    (-1.896e0 - 4.808e0j, 1.806e0 + 4.563e0j),
                    (-9.396e0 - 6.477e0j, 1.443e0 - 8.219e1j),
                ]
            ]
        )
        self.frequency_range = (0.1 / h, 5 / h)


class Au(Medium):
    """Gold

    Refs:
    * P. B. Johnson and R. W. Christy. Optical constants of the noble metals, Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (8.49850999e-01 + 2.38196361e00j, -5.66237335e00 + 1.12777669e00j),
                    (6.75243395e-01 - 2.91053060e-01j, 2.39735878e00 - 3.00926970e-02j),
                    (
                        -2.61132076e-02 + 5.13313035e-01j,
                        -7.17394175e00 - 7.98759571e00j,
                    ),
                    (
                        -6.14960965e-01 - 2.95818181e-01j,
                        -2.77674273e00 + 3.30485297e01j,
                    ),
                    (
                        -3.11626658e-01 - 5.75388095e-01j,
                        -1.73738214e01 - 2.61164682e-01j,
                    ),
                    (3.02683713e-01 - 4.76159587e-01j, 2.04533591e01 + 9.52125189e00j),
                ]
            ]
        )
        self.frequency_range = (0.64 / h, 6.6 / h)


class Cu(Medium):
    """Copper

    Refs:
    * P. B. Johnson and R. W. Christy. Optical constants of the noble metals, Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (1.03838239e01 + 3.20912171e00j, 6.38760254e01 + 2.07202180e02j),
                    (
                        -5.33894815e-02 + 1.75492880e-01j,
                        -5.64580041e00 - 1.12906254e02j,
                    ),
                    (6.28372739e00 + 2.14152243e-01j, -8.56946907e01 - 1.39095249e02j),
                    (6.29840983e-01 + 5.03348708e00j, 7.15178521e-02 - 8.70614823e-01j),
                    (2.81529785e-01 + 2.13298112e00j, -1.25431373e00 + 2.26098107e-01j),
                    (1.57717671e-01 + 2.33922716e-01j, 5.79456919e00 - 7.44449555e01j),
                ]
            ]
        )
        self.frequency_range = (0.64 / h, 6.6 / h)


class Al(Medium):
    """Aluminum

    Refs:
    * A. D. Rakic. Algorithm for the determination of intrinsic optical
      constants of metal films: application to aluminum,
      Appl. Opt. 34, 4755-4767 (1995)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (2.08620529e-03 + 5.17004564e-03j, 1.82699161e02 + 1.22808170e04j),
                    (
                        -5.61340366e-02 - 3.67626556e-02j,
                        -5.52211024e02 + 5.14063171e01j,
                    ),
                    (3.87899126e-02 - 1.29401976e-04j, 6.25983960e02 + 8.40290290e05j),
                    (2.76007598e-01 + 1.54849458e00j, -1.84239452e00 - 1.00308670e01j),
                    (1.81020958e-01 + 7.46192964e-02j, -2.57949907e02 - 4.13667452e02j),
                ]
            ]
        )
        self.frequency_range = (0.1 / h, 10 / h)


class Be(Medium):
    """Beryllium

    Refs:
    * A. D. Rakic. Algorithm for the determination of intrinsic optical
      constants of metal films: application to aluminum,
      Appl. Opt. 34, 4755-4767 (1995)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (6.88444175e-02 - 6.94278821e-03j, 1.88350836e02 - 6.02535134e02j),
                    (2.89861208e-03 + 1.35182137e-02j, -1.96334578e02 - 3.56842389e02j),
                    (4.80608285e00 - 9.35652870e-01j, 8.06504906e01 + 4.85161848e02j),
                    (-4.11762893e00 + 3.38498642e00j, 3.79764137e01 + 5.62724724e00j),
                    (6.08678571e01 + 1.25948706e01j, 3.58400307e03 - 1.75611583e04j),
                ]
            ]
        )
        self.frequency_range = (0.1 / h, 10 / h)


class Cr(Medium):
    """Chromium

    Refs:
    * A. D. Rakic. Algorithm for the determination of intrinsic optical
      constants of metal films: application to aluminum,
      Appl. Opt. 34, 4755-4767 (1995)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        -4.11784686e-03 + 8.77345194e-05j,
                        -1.66350239e02 + 4.10231058e03j,
                    ),
                    (-2.16265322e00 + 3.90143428e01j, -1.97925747e02 + 2.96158245e01j),
                    (7.63173243e00 + 1.07867249e01j, -3.97047485e02 - 1.43134376e03j),
                    (7.26476770e00 + 1.00344818e01j, 5.04950821e02 + 1.21726971e03j),
                    (1.34470084e00 - 1.61652707e00j, 1.05387797e01 + 3.78274623e01j),
                    (5.53024713e-02 - 1.42953408e-02j, 1.57827383e02 - 4.22023181e01j),
                ]
            ]
        )
        self.frequency_range = (0.1 / h, 10 / h)


class Ni(Medium):
    """Nickel

    Refs:
    * P. B. Johnson and R. W. Christy. Optical constants of the noble metals, Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (1.25355476e00 - 1.49630304e00j, 5.65016005e00 - 2.59942051e-01j),
                    (2.78009815e02 + 8.71683358e00j, 3.75280066e03 + 1.09392965e04j),
                    (-3.57849446e00 - 4.18985698e-04j, 2.90571138e01 - 1.77250076e05j),
                    (8.35074504e-01 + 4.50988641e00j, -1.02236287e00 - 3.14255906e00j),
                    (-1.10273187e01 + 1.11212052e01j, 3.47711480e02 + 1.59920866e02j),
                    (6.56287149e-02 + 3.86669672e-04j, -1.53841624e01 - 3.63792384e04j),
                ]
            ]
        )
        self.frequency_range = (0.64 / h, 6.6 / h)


class Pd(Medium):
    """Palladium

    Refs:
    * P. B. Johnson and R. W. Christy. Optical constants of the noble metals, Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (4.43711404e00 + 5.97754021e-02j, -6.47156562e01 + 3.44470903e03j),
                    (2.80153697e01 + 6.64369598e-02j, 1.18522076e03 + 8.27481558e03j),
                    (-2.33753426e01 - 6.27298716e01j, 1.31302184e04 + 1.52841559e03j),
                    (1.64512424e02 - 1.50248387e02j, -9.26539444e03 - 3.31902450e04j),
                    (-1.37446584e01 + 3.43404962e03j, -8.80267177e06 - 7.70380100e04j),
                    (2.29336292e-02 + 9.28898717e-04j, -2.01618270e01 - 1.73587917e04j),
                ]
            ]
        )
        self.frequency_range = (0.64 / h, 6.6 / h)


class Pt(Medium):
    """Platinum

    Refs:
    * W. S. M. Werner, K. Glantschnig, C. Ambrosch-Draxl.
      Optical constants and inelastic electron-scattering data for 17
      elemental metals, J. Phys Chem Ref. Data 38, 1013-1092 (2009)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (-1.35259673e02 + 2.26232980e02j, -8.82907650e04 + 3.47684416e03j),
                    (3.51775024e-01 - 3.35220153e00j, -1.12793517e00 + 1.36004192e00j),
                    (3.62948285e01 + 2.80930804e02j, 8.40046239e02 - 1.15741537e04j),
                    (1.51469860e00 + 1.37002598e-02j, -9.31593110e-01 + 1.86950566e03j),
                    (7.34775338e-02 - 1.37071581e-02j, -9.74006342e00 + 6.12067411e03j),
                    (3.27181650e02 + 1.48990025e02j, -1.80856542e04 - 8.49492237e04j),
                ]
            ]
        )
        self.frequency_range = (C_0 / 0.1, C_0 / 2.48)


class Ti(Medium):
    """Titanium

    Refs:
    * W. S. M. Werner, K. Glantschnig, C. Ambrosch-Draxl.
      Optical constants and inelastic electron-scattering data for 17
      elemental metals, J. Phys Chem Ref. Data 38, 1013-1092 (2009)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        -7.30813382e-03 + 4.95376765e-01j,
                        -3.29382184e00 + 5.57830947e-0j,
                    ),
                    (4.50075809e-01 + 1.00006334e00j, 1.07470580e01 - 5.23505055e00j),
                    (6.81187707e-01 - 3.24561397e00j, -2.94240521e00 + 1.52487228e00j),
                    (4.88392282e-03 + 7.49800235e-01j, -2.96725141e00 - 1.01812500e00j),
                    (
                        -1.98528708e-01 - 3.13533640e-01j,
                        -1.04745592e01 + 1.13013261e02j,
                    ),
                    (
                        -2.03288860e-03 + 7.44239733e-01j,
                        -2.06486776e-01 - 4.20393124e00j,
                    ),
                ]
            ]
        )
        self.frequency_range = (C_0 / 0.1, C_0 / 2.48)


class W(Medium):
    """Tungsten

    Refs:
    * W. S. M. Werner, K. Glantschnig, C. Ambrosch-Draxl.
      Optical constants and inelastic electron-scattering data for 17
      elemental metals, J. Phys Chem Ref. Data 38, 1013-1092 (2009)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (6.31773122e-01 + 3.08163758e00j, 1.09644858e02 - 1.01956518e02),
                    (2.18082553e00 + 2.31873569e-04j, 1.03952714e01 + 3.01294371e05j),
                    (-6.69721537e-02 + 6.62226412e-02j, 2.23181154e02 - 1.08845104e03j),
                    (
                        -3.43257695e-02 + 1.97474191e-01j,
                        -2.37823552e02 - 5.55451714e01j,
                    ),
                    (6.30448295e-01 + 3.14958595e00j, -1.15401617e02 + 8.05913282e01j),
                    (2.41888942e-01 + 9.59566518e-01j, -2.77211758e00 - 2.62038460e01j),
                ]
            ]
        )
        self.frequency_range = (C_0 / 0.1, C_0 / 2.48)


class InP(Medium):
    """Indium Phosphide

    Refs:
    * G. D. Pettit and W. J. Turner. Refractive index of InP,
      J. Appl. Phys. 36, 2081 (1965)
    * A. N. Pikhtin and A. D. Yaskov. Disperson of the refractive index of
      semiconductors with diamond and zinc-blende structures,
      Sov. Phys. Semicond. 12, 622-626 (1978)
    * Handbook of Optics, 2nd edition, Vol. 2. McGraw-Hill 1994
    """

    def __init__(self, variant=None):
        self.eps = 7.255
        self.sigma = 0

        if variant is None:
            variant = "Pettit1965"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Pettit1965" == variant:
            self.dispmod = Sellmeier(
                [
                    (2.316, 0.6263 ** 2),
                    (2.765, 32.935 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 10, C_0 / 0.95)


class Ge(Medium):
    """Germanium

    Refs:
    * Icenogle et al.. Refractive indexes and temperature coefficients of
      germanium and silicon Appl. Opt. 15 2348-2351 (1976)
    * N. P. Barnes and M. S. Piltch. Temperature-dependent Sellmeier
      coefficients and nonlinear optics average power limit for germanium
      J. Opt. Soc. Am. 69 178-180 (1979)
    """

    def __init__(self, variant=None):
        self.eps = 9.28156
        self.sigma = 0

        if variant is None:
            variant = "Icenogle1976"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Icenogle1976" == variant:
            self.dispmod = Sellmeier(
                [
                    (6.72880, 0.44105),
                    (0.21307, 3870.1),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 12, C_0 / 2.5)


class YAG(Medium):
    """Yttrium aluminium garnet

    Refs:
    * D. E. Zelmon, D. L. Small and R. Page.
      Refractive-index measurements of undoped yttrium aluminum garnet
      from 0.4 to 5.0 um, Appl. Opt. 37, 4933-4935 (1998)
    """

    def __init__(self, variant=None):
        self.eps = 1
        self.sigma = 0

        if variant is None:
            variant = "Zelmon1998"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Zelmon1998" == variant:
            self.dispmod = Sellmeier(
                [
                    (2.28200, 0.01185),
                    (3.27644, 282.734),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 5, C_0 / 0.4)
