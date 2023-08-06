import numpy 

class width:
    def __init__(self):
        # quark masses from PDG 2020
        self.quark_mass = [
            0.00216, # up
            0.00467, # down
            0.093,   # strange
            1.27,    # charm
            4.18,    # bottom
            172.76   # top
        ]
        # lepton masses: e mu tau from PDG 2020
        self.lepton_mass = [0.000511, 0.105658, 1.77682]
        self._vev = 246
        # fermion-Yukawa-Coupling function 
        self._fyc = lambda mf: np.sqrt(2)*mf/self.vev
        
    # Vector mediators
    def vector_qq(self, med_mass, g=1.0):
        """ Width of vector mediator decaying to quarks        
        """
        width = 0
        for mass in self.quark_mass:
            z = np.divide(mass, med_mass)**2
            width += np.where(
                med_mass >= 2 * mass,
                g**2 * med_mass * np.sqrt(1 - 4*z) * (1 + 2*z) / (4*np.pi),
                0.0 
            )
        return width

    def vector_ll(self, med_mass, g=1.0):
        """Width of vector mediator decaying to leptons
        """
        width = 0
        for mass in self.lepton_mass:
            z = np.divide(mass, med_mass)**2
            width += np.where(
                med_mass >= 2 * mass,
                g**2 * med_mass * np.sqrt(1 - 4*z) * (1 + 2*z) / (12*np.pi),
                0.0 
            )
        return width

    def vector_nn(self, med_mass, g=1.0):
        """Width of vector mediator decaying to neutrinos
        """
        return 3 * np.where(
            med_mass >= 2 * mass, 
            g**2 * med_mass / (24*np.pi),
            0.0
        )

    def vector_dm(self, med_mass, chi_mass=1.0, g=1.0):
        """Width of vector mediator decaying to dark matter candidates 
        """
        z = np.divide(chi_mass, med_mass)**2
        return np.where(
            med_mass >= 2 * mass, 
            g**2 * med_mass * np.sqrt(1 - 4*z) * (1 + 2*z) / (12*np.pi),
            0.0
        )

    def vector_total_width(self, med_mass, chi_mass, g_q=0.25, g_chi=1.0, g_l=0.0):
        """Total width of the vector mediator
        """
        total  = vector_qq(med_mass, g_q)
        total += vector_ll(med_mass, g_l)
        total += vector_nn(med_mass, g_l)
        total += vector_dm(med_mass, chi_mass, g_chi)
        return total
    
    #Axial-Vector Mediators
    def axial_qq(self, med_mass, g = 1.0):
        width = 0
        for mass in self.quark_mass:
            z = np.divide(mass, med_mass)**2
            width += np.where(
                med_mass >= 2 * mass,
                g**2 * med_mass * np.sqrt(1 - 4*z)**3 / (4*np.pi),
                0.0 
            )
        return width

    def axial_ll(self, med_mass, g = 1.0):
        width = 0
        for mass in self.lepton_mass:
            z = np.divide(mass, med_mass)**2
            width += np.where(
                med_mass >= 2 * mass,
                g**2 * med_mass * np.sqrt(1 - 4*z)**3 / (12*np.pi),
                0.0 
            )
        return width

    def axial_nn(self, med_mass, g = 1.0):
        return 3 * np.where(
            med_mass >= 2 * mass, 
            g**2 * med_mass / (24*np.pi),
            0.0
        )

    def axial_dm(self, med_mass, chi_mass=1.0, g = 1.0):
        z = np.divide(chi_mass, med_mass)**2
        return np.where(
            med_mass >= 2 * mass, 
            g**2 * med_mass * np.sqrt(1 - 4*z)**3 / (12*np.pi),
            0.0
        )

    def axial_total_width(self, med_mass, chi_mass, g_q=0.25, g_dm=1.0, g_l=0.0):
        total  = axial_qq(med_mass, g_q)
        total += axial_ll(med_mass, g_l)
        total += axial_nn(med_mass, g_l)
        total += axial_dm(med_mass, chi_mass, g_dm)
        return total

    # Scalar Mediators
    def form_factor_s(tau):
        return tau * (
            1 + (1 - tau)* np.arctan(np.devide(1, np.sqrt(tau - 1)))**2
        )
    def from_factor_ps(tau):
        return tau * np.arctan(np.devide(1, np.sqrt(tau - 1)))**2

    def scalar_qq(self, med_mass, g=1.0):
        width = 0
        for mass in self.quark_mass:
            z = np.divide(mass, med_mass)**2
            width += np.where(
                med_mass >= 2 * mass,
                3 * g**2 * self._fyk(mass)**2 * med_mass * np.sqrt(1 - 4*z)**3 / (16*np.pi),
                0.0
            )
        return width

    # TODO: Finish implementing all the different functions for scalar and pseudo-scalar med

       


