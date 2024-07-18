# Fritsch Solitons Requirements Specification
Author: Joshua D. JOHN

Date: 2024/04/18

What I am calling the Fritsch method is a way to create dark solitons at arbitrary position and velocity by simultaneously engineering the amplitude and phase of the condensate wave function. This is supposed to be a better approach compared to the technique we demonstrated before which manipulated the condensate phase only.

* Fritsch, A.R., Lu, M., Reid, G., Piñeiro, A., & Spielman, I.B. (2020). Creating solitons with controllable and near-zero velocity in Bose-Einstein condensates. Physical review. A, 101 5.


## Outline
* Features
* API
    * Function Name
    * Usage
* Usage Examples

## Features
* Creates a job that can be submitted to the Oqtant Quantum Matter Service. This job is a completeley prepared quantum matter with its landscapes, snapshots and lasers already set.
* Provides a way to set the imprinting phase that will be used to imprint half of the dimple and generate the desired solitonic behavior.
*  An internal algorithm uses the specified phase and other internal information on dimple preparation, evolution duration, time-of-flight duration to prepare quantum matter landscapes, snapshots and lasers and produce a submittable job.

## API
### Name
#### _FritschSoliton(qmf)_
##### Usage
This function creates a FritschSoliton object which uses the Oqtant Quantum Matter Factory _qmf_.
Requires a valid Quantum Matter Factory object. In this state the object is initialized with default phase (pi) and evolution time (50 ms). Calling the object's _get_matter()_ function prepares the quantum matter landscapes, snapshots and lasers and returns a complete submittable job. 

#### _FritschSoliton(qmf, phase, evolution_time)_
##### Usage
This function creates a FritshSolition object which uses the Oqtant Quantum Matter Factory _qmf_. This construction also directly initializes the object with the imprinting phase and evolution time. Calling the object's _get_matter()_ function prepares the quantum matter landscapes, snapshots and lasers and returns a complete submittable job.

#### _FritschSoliton.set_imprinting_phase(phase)_
##### Usage
This function allows setting or changing the phase of the FritschSoliton object. The specified phase is immediately set. Calling the object's _get_matter()_ function prepares the quantum matter landscapes, snapshots and lasers and returns a complete submittable job.

#### _FritschSoliton.set_evolution_time(evolution_time)_
##### Usage
This function allows setting or changing the evolution time of the FritschSoliton object. The specified evolution time is immediately set. Calling the object's _get_matter()_ function prepares the quantum matter landscapes, snapshots and lasers and returns a complete submittable job.

#### _FritschSoliton.get_matter()_
##### Usage
This function  returns as completely prepared quantum matter object, which can be directly submitted to the Oqtant service. The prepared quantum matter is prepared according to the Fritsch imprinting sequences described in the paper referenced above.

## Usage Examples
```python
    qmf = QuantumMatterFactory()
    qmf.get_login()

    fs = FritschSoliton(qmf)

    phi = 1 # in pi units
    fs.set_imprinting_phase(phi)

    ev_time = 50 # ms
    fs.set_evolution_time(ev_time)

    matter = ps.get_matter()

    matter.submit(sim=True)
    ```