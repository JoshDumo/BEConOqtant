# Fritsch Solitons Requirements Specification
Author: Joshua D. JOHN

Date: 2024/04/18

What I am calling the Fritsch method is a way to create dark solitons at arbitrary position and velocity by simultaneously engineering the amplitude and phase of the condensate wave function. This is introduced as a better approach compared to the technique demonstrated before, which manipulated the condensate phase only.

* Fritsch, A.R., Lu, M., Reid, G., Piñeiro, A., & Spielman, I.B. (2020). _Creating solitons with controllable and near-zero velocity in Bose-Einstein condensates._ Physical review. A, 101 5.


## Outline
* Features
* API
    * Function Name
    * Usage
* Usage Examples

## Features
* Creates a job that can be submitted to the Oqtant Quantum Matter Service. This job is a completeley prepared quantum matter with its landscapes, snapshots and lasers already set.
* Provides a way to set the imprinting phase that will be used to imprint half of the BEC and generate the desired solitonic behavior.
* Provides a way to set the potential that will be used to adiabatically create the dimple before phase imprinting, and to adiabatically release the dimple after phase imprinting. 
* Provides a way to set the time after evolution to release the BEC for its 15ms drop before Time-of-Flight imaging.
*  An internal algorithm uses the specified phase and other internal information to prepare quantum matter landscapes, snapshots and lasers and produce a submittable job.

## API
### Name
#### _FritschSoliton(qmf)_
##### Usage
This function creates a FritschSoliton object which uses the Oqtant Quantum Matter Factory _qmf_.
Requires a valid Quantum Matter Factory object. 

In this state the object is initialized with defaults
* dimpling potential (0.5 kHz),
* imprinting phase ($\pi$), and 
* hold after evolution before drop time (0 ms). 

Calling the object's _get_matter()_ function prepares the quantum matter landscapes, snapshots and lasers and returns a complete submittable job. 

#### _FritschSoliton(qmf, dimple_potential, imprinting_phase, hold_time)_
##### Usage
This function creates a FritshSolition object which uses the Oqtant Quantum Matter Factory _qmf_. 

This construction also directly initializes the object with the specified dimpling potential, imprinting phase and evolution hold time. 

Calling the object's _get_matter()_ function prepares the quantum matter landscapes, snapshots and lasers and returns a complete submittable job.

#### _FritschSoliton.set_dimpling_potential(potential)_
##### Usage
This function allows setting or changing the dimpling potential of the FritschSoliton object. The potential can be set within the range [0, 0.5] kHz. The specified potential is immediately set. 

Calling the object's _get_matter()_ function prepares the quantum matter landscapes, snapshots and lasers and returns a complete submittable job.

#### _FritschSoliton.set_imprinting_phase(phase)_
##### Usage
This function allows setting or changing the phase of the FritschSoliton object. The imprinting phase is set (in units of $\pi$) in the range [1, 2] $\pi$. The specified phase is immediately set. 

Calling the object's _get_matter()_ function prepares the quantum matter landscapes, snapshots and lasers and returns a complete submittable job.

#### _FritschSoliton.set_hold_time(hold_time)_
##### Usage
This function allows setting or changing the hold time after evolution of the FritschSoliton object. The hold time can be set in the range [0, 20] ms.The specified evolution time is immediately set. 

Calling the object's _get_matter()_ function prepares the quantum matter landscapes, snapshots and lasers and returns a complete submittable job.

#### _FritschSoliton.get_matter()_
##### Usage
This function  returns as completely prepared quantum matter object, which can be directly submitted to the Oqtant service. The prepared quantum matter is prepared according to the Fritsch imprinting sequences described in the paper referenced above. 

The potential is set to ramp up to the set _dimpling potential_ from 0 to 15 ms. Afterwards, the ponetial drops to 0 and holds for 100 $\mu$ s. The potential is then set to a step potential over half of the BEC, the potential set to a value that achieves the desired phase imprinting. The potential is flashed for 0.7 ms. Finally the dimple potential is applied and ramped down for 3 ms. After this sequence, the BEC is left to evolve in trap for 80 ms. After this evolution, the potential is held for an additional _hold_time_ before being released from the trap to expand for 15 ms before being TOF imaged. 

## Usage Examples
```python
    qmf = QuantumMatterFactory()
    qmf.get_login()

    fs = FritschSoliton(qmf)

    phi = 1.1 # in pi units
    fs.set_imprinting_phase(phi)

    ev_time = 10.0 # ms
    fs.set_evolution_time(ev_time)

    matter = fs.get_matter()

    matter.submit(sim=True)
    ```