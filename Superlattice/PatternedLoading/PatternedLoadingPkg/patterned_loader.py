"""
    Sets up and prepared quantum matter for patterned loading
"""
import numpy as np
import matplotlib.pyplot as plt

from .utils import range_validator


class PatternedLoader:
    """
    Sets up and prepared quantum matter for patterned loading
    
    Attributes:
        qmf (quantum matter object) : an Oqtant quantum matter factory 
        matter_name (str) : matter name
    """
    def __init__(self, qmf, matter_name="Superlattice"):
        self.qmf = qmf
        self.matter_name = matter_name
        self.short_lattice = self.Lattice()
        self.long_lattice = self.Lattice()
    
    class Lattice:
        """
        Sets up a lattice's dynamics for patterned loading

        Attributes:
            potential (double) : potential peak for the lattice
            delay (double) : from the start, delay time
            rise (double) : from end of delay, how fast the potential rises from 0 to peak
            hold (double) : after rising, how long to hold the potential before fall 
                rise and fall is the same

        """
        LATTICE_TIME = 6 #ms
        def __init__(self, potential=0., delay=0., rise=0., hold=0.):
            range_validator(potential, "potential", 0, 100.0)
            self.potential = potential
            
            range_validator(delay, "delay", 0, 5.0)
            self.delay = delay
            
            range_validator(rise, "rise", 0, 3.0)
            self.rise = rise
            
            range_validator(hold, "hold", 0, 5.0)
            self.hold = hold
        
        def set_potential(self, potential):
            """
            Sets the lattice potential.

            """
            range_validator(potential, "potential", 0, 100.0)
            self.potential = potential
            
        def set_loading_seq(self, delay, rise, hold):
            """
            Sets the lattice potential timings.
            """
            range_validator(delay, "delay", 0, 5.0)
            self.delay = delay
            
            range_validator(rise, "rise", 0, 3.0)
            self.rise = rise
            
            range_validator(hold, "hold", 0, 5.0)
            self.hold = hold
            
        def __gaussian__(self, x, mu, sig, a):
            return a * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    
        def __flat_pot__(self, x, a):
            return a * np.ones(len(x))
        
        def __prepare_timepot_seq__(self, peak, delay, rise, hold):
            div = 0.3
            assert delay+rise+hold <= self.LATTICE_TIME, f"sum(delay, rise,hold) {delay+rise+hold} greater than {self.LATTICE_TIME} ms" 
            delay_nits = np.linspace(0, delay, int(delay/div))
            delay_pot = self.__flat_pot__(delay_nits, 0)
        
            rise_nits = np.linspace(delay+div, rise+delay, int(rise/div))
            rise_pot = self.__gaussian__(rise_nits, rise+delay, rise/(2.355*1.5), peak)
        
            hold_nits = np.linspace(rise+delay+div, hold+rise+delay, int(hold/div))
            hold_pot = self.__flat_pot__(hold_nits, peak)
        
            total_time = np.append(delay_nits, rise_nits)
            total_time = np.append(total_time, hold_nits)
        
            total_pot = np.append(delay_pot, rise_pot)
            total_pot = np.append(total_pot, hold_pot)
        
            if delay+2*rise+hold <= self.LATTICE_TIME:
                fall_nits = np.linspace(hold+rise+delay+div, rise+hold+rise+delay, int(rise/div))
                fall_pot = self.__gaussian__(fall_nits, hold+rise+delay, rise/(2.355*1.5), peak)
                total_time = np.append(total_time, fall_nits)
                total_pot = np.append(total_pot, fall_pot)
        
            total_time = np.round(total_time, 1)
            return total_time, total_pot
        
        def get_lattice_dynamics(self):
            """
            Get the potential v. time sequence for the lattice
            """
            times, pots = self.__prepare_timepot_seq__(self.potential, 
                                                       self.delay, 
                                                       self.rise, 
                                                       self.hold
                                               )
            return times, pots
            
            
    def set_superlattice(self, long, short):
        """
        Sets the long and short lattices that compose the superlattice

        """
        self.short_lattice = short
        self.long_lattice = long

    def show_superlattice_dynamics(self):
        """
        Plots the long and short lattice dynamics of the superlattice

        """
        lt, lp = self.long_lattice.get_lattice_dynamics()
        st, sp = self.short_lattice.get_lattice_dynamics()
        plt.plot(lt, lp)
        plt.plot(st, sp)
     
    def get_matter(self, matter_name="lattices"):
        """
        Prepares and returns a pattern loaded quantum matter sequence ready to be submitted to Oqtant
        """
        self.matter_name = matter_name
        times_l, pots_l = self.long_lattice.get_lattice_dynamics()
        times_l, pots_l = self.short_lattice.get_lattice_dynamics()

        pos_l = np.arange(-12,12,6)
        pos_l = np.arange(-6,6,2)
        barriers = []
        for pos in pos_l:
            poss = pos*np.ones(len(times_l))
            wids = 1.5*np.ones(len(times_l))
            barr = self.qmf.create_barrier(positions=poss,
                                     heights=pots_l,
                                     widths=wids,
                                     times=times_l,
                                     shape="GAUSSIAN",
                                    )
            barriers.append(barr)
        for pos in pos_l:
            poss = pos*np.ones(len(times_l))
            wids = 0.5*np.ones(len(times_l))
            barr = self.qmf.create_barrier(positions=poss,
                                     heights=pots_l,
                                     widths=wids,
                                     times=times_l,
                                     shape="SQUARE",
                                    )
            barriers.append(barr)
        
        matter = self.qmf.create_quantum_matter(temperature=100,
                                                lifetime=6,
                                                time_of_flight=8,
                                                barriers=barriers,
                                                image="IN_TRAP",
                                                name=self.matter_name,
                                               )
        return matter
    