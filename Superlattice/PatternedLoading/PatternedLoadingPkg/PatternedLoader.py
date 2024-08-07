from .utils import RangeValidator
import numpy as np

class PatternedLoader:
    def __init__(self, qmf, matter_name="Superlattice"):
        self.qmf = qmf
        self.matter_name = matter_name
        self.short_lattice = self.Lattice()
        self.long_lattice = self.Lattice()
    
    class Lattice:
        def __init__(self, potential=0., delay=0., rise=0., hold=0.):
            RangeValidator(potential, "potential", 0, 20.0)
            self.potential = potential
            
            RangeValidator(delay, "delay", 0, 5.0)
            self.delay = delay
            
            RangeValidator(rise, "rise", 0, 3.0)
            self.rise = rise
            
            RangeValidator(hold, "hold", 0, 5.0)
            self.hold = hold
        
        def set_potential(self, potential):
            RangeValidator(potential, "potential", 0, 20.0)
            self.potential = potential
            
        def set_loading_seq(self, delay, rise, hold):
            RangeValidator(delay, "delay", 0, 5.0)
            self.delay = delay
            
            RangeValidator(rise, "rise", 0, 3.0)
            self.rise = rise
            
            RangeValidator(hold, "hold", 0, 5.0)
            self.hold = hold
            
        def print_lattice(self):
            print("potential:", self.potential)
            
    def set_superlattice(self, long, short):
        self.short_lattice = short
        self.long_lattice = long
    
    def print_superlattice(self):
        print("short pot:", self.short_lattice.potential)
        print("long pot:", self.long_lattice.potential)
        
    def __gaussian__(self, x, mu, sig, A):
        return A * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
    
    def __flat_pot__(self, x, A):
        return A * np.ones(len(x))
    
    def __prepare_timepot_seq__(self, peak, delay, rise, hold):
        LATTICE_TIME = 6. #ms
        div = 0.3
        assert delay+rise+hold <= LATTICE_TIME, f"sum(delay, rise,hold) {delay+rise+hold} greater than {LATTICE_TIME} ms" 
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
    
        if delay+2*rise+hold <= LATTICE_TIME:
            fall_nits = np.linspace(hold+rise+delay+div, rise+hold+rise+delay, int(rise/div))
            fall_pot = self.__gaussian__(fall_nits, hold+rise+delay, rise/(2.355*1.5), peak)
            total_time = np.append(total_time, fall_nits)
            total_pot = np.append(total_pot, fall_pot)
    
        total_time = np.round(total_time, 1)
        return total_time, total_pot
    
    def get_matter(self):
        timesL, potsL = self.__prepare_timepot_seq__(self.long_lattice.potential, 
                                                self.long_lattice.delay, 
                                                self.long_lattice.rise, 
                                                self.long_lattice.hold
                                               )
        timesS, potsS = self.__prepare_timepot_seq__(self.short_lattice.potential, 
                                                self.short_lattice.delay, 
                                                self.short_lattice.rise, 
                                                self.short_lattice.hold
                                               )
        posL = np.arange(-12,12,6)
        posS = np.arange(-6,6,2)
        barriers = []
        for pos in posL:
            poss = pos*np.ones(len(timesL))
            wids = 1.5*np.ones(len(timesL))
            bar = self.qmf.create_barrier(positions=poss,
                                     heights=potsL,
                                     widths=wids,
                                     times=timesL,
                                     shape="GAUSSIAN",
                                    )
            barriers.append(bar)
        for pos in posS:
            poss = pos*np.ones(len(timesL))
            wids = 0.5*np.ones(len(timesL))
            bar = self.qmf.create_barrier(positions=poss,
                                     heights=potsS,
                                     widths=wids,
                                     times=timesS,
                                     shape="SQUARE",
                                    )
            barriers.append(bar)
        
        matter = self.qmf.create_quantum_matter(temperature=100,
                                                lifetime=6,
                                                time_of_flight=10,
                                                barriers=barriers,
                                                image="IN_TRAP",
                                                name=self.matter_name,
                                               )
        return matter
    