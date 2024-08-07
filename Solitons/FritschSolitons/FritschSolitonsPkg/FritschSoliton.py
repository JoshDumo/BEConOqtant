from .utils import RangeValidator

class FritschSolitonMatter:
    def __init__(self, 
                 qmf, 
                 soliton_position = 1.0,
                 dimpling_potential = 1.0, 
                 imprinting_phase = 1.0 , 
                 hold_time = 0, 
                 matter_name = "fritsch sol"):
        self.qmf = qmf

        RangeValidator(soliton_position, "soliton_position", -20.0, 20.0)
        self.soliton_position = soliton_position

        RangeValidator(dimpling_potential, "dimpling_potential", 0.0, 2.0)
        self.dimpling_potential = dimpling_potential
        
        RangeValidator(imprinting_phase, "imprinting_phase", 0, 2.0)
        self.imprinting_phase = imprinting_phase
        
        RangeValidator(hold_time, "hold_time", 0, 60.0)
        self.hold_time = hold_time
        self.matter_name = matter_name

    def set_position(self, soliton_position):
        RangeValidator(soliton_position, "soliton_position", -20.0, 20.0)
        self.soliton_position = soliton_position
        
    def set_imprinting_phase(self, imprinting_phase):
        RangeValidator(imprinting_phase, "imprinting_phase", 0, 2.0)
        self.imprinting_phase = imprinting_phase
        
    def set_dimpling_potential(self, dimpling_potential):
        RangeValidator(dimpling_potential, "dimpling_potential", 0.0, 2.0)
        self.dimpling_potential = dimpling_potential
        
    def set_hold_time(self, hold_time):
        RangeValidator(hold_time, "hold_time", 0, 60.0)
        self.hold_time = hold_time
    
        
    def get_matter(self):
        dV = self.dimpling_potential
        t_p = 1.0 #ms
        phV = self.imprinting_phase / (2*t_p) # U/h = phi/(2*t_p)
        dW = 2.0 #micron
        pos = self.soliton_position
        tof = 10 #ms
        intrap = 40 #ms
        temp = 100 #nK
        evol_time = intrap + self.hold_time
        ramp_up = self.qmf.create_barrier(
            positions=[pos, pos, pos],
            heights=[0, dV, 0],
            widths=[dW, dW, dW],
            times=[0, 15, 15.1],
            shape="GAUSSIAN",
        )

        # phase imprint ne snapshot
        positions = [-60, 0, 0, 60]
        heights_ramp = [0, 0, phV, phV]
        snapshot_zero = self.qmf.create_snapshot(
            time=15.2, positions=positions, potentials=heights_ramp, interpolation="LINEAR"
        )
        snapshot_one = self.qmf.create_snapshot(
            time=15.9,
            positions=[0, 0],
            potentials=[0, 0],
            interpolation="LINEAR",
        )
        phaser = self.qmf.create_landscape(snapshots=[snapshot_zero, snapshot_one])

        ramp_down = self.qmf.create_barrier(
            positions=[pos, pos, pos],
            heights=[0, dV, 0],
            widths=[dW, dW, dW],
            times=[16.0, 16.1, 19.1],
            shape="GAUSSIAN",
        )
        
        fritsch_sol = self.qmf.create_quantum_matter(
            temperature=temp,
            lifetime=evol_time,
            time_of_flight=tof,
            barriers=[ramp_up, ramp_down],
            landscape=phaser,
            name=self.matter_name,
        )
        
        return fritsch_sol