# Patterned Loading Requirements Specification 
This feature creates a superlattice potential over a BEC. Two independent lattices are applied in sequence over the BEC. Depending on the potentials and periods of the lattices, the BEC atoms can be selectively loaded or confined to some sites, and removed in others. This technique is referred to as Patterned Loading.

* Peil, S.E., Porto, J.V., Tolra, B.L., Obrecht, J.M., King, B.E., Subbotin, M., Rolston, S., & Phillips, W.D. (2003). Patterned loading of a Bose-Einstein condensate into an optical lattice. Physical Review A, 67, 051603.

## Outline
* Features
* API
    * Function Name
    * Usage
* Usage Example

### Features
* Creates a job that can be submitted to the Oqtant Quantum Matter Service. This job is a completeley prepared quantum matter with its landscapes, snapshots and lasers already set.
* Provides a way to set the potential profile for the superlattice of two independent sinusoidal lattices.
* Provides a way to prepare a general sinusoidal lattice specified by its potential amplitude. The prepared superlattice potential will be 
    $$ U(z) = - \frac{U_{long}}{2}cos(2 \pi z /d_{long}) - \frac{U_{short}}{2}cos(2 \pi z /d_{short} + \phi)$$

    The potentials will be loaded in a sequence as specified by the loading sequence for each independent lattice.

* Provides a way to prepare a loading sequence for each independent lattice. The loading sequence is specified by a pulse with parameters of delay, rise time, and hold.
    
* An internal algorithm uses the specified two independent lattices to prepare quantum matter landscapes, snapshots and lasers and produce a submittable job.

### API
#### Name
##### _PatternedLoader(qmf)_
#### Usage
This function creates a Patterned Loader object which uses the Oqtant Quantum Matter Factory _qmf_.
Requires a valid Quantum Matter Factory object.

#### Name
##### _PatternedLoader(qmf).set_superlattice(long, short)_
#### Usage
This function sets the superlattice from two independent sinusoidal lattices _long_ and _short_. The preparation of independent lattices is provided by the services:
1. _PatternedLoader(qmf).Lattice(potential, delay, rise_time, hold)_, or
2.  
    a. _PatternedLoader(qmf).Lattice().set_potential(potential)_, and 
    
    b. _PatternedLoader(qmf).Lattice().set_loading_seq(delay, rise_time, hold)_

#### Parameters
###### _potential_
The peak potential of the independent lattice. During loading, the potential will be  swept from zero to peak, and back again to zero as specified by the loading sequence parameters _delay, rise_time and hold_.

Ranges from 0 to 20 KHz (determined by max of Oqtant service).

##### _delay_
Duration from zero before the start of the rising edge of the loading sequence.
Ranges from 0 to 5 ms. It should still be possible to raise and fall an edge right to the max of the loading sequence 6ms.

##### _rise_time_
The transition time from 0 to peak potential, and from peak back to 0, 100us resolution. The edge is symmetric for rising and falling. The falling pulse is ignored if the hold time is set longer than 5ms.

##### _hold_
The duration to hold the peak potential after rising and before start of falling. To set a hold beyond the time sequence 
Ranges from 0 to 5ms. A hold time longer than 5ms implies hold until lifetime, and no fall time

Combination of _delay, rise_time, and hold_ should be less than or equal to 6ms, the total duration of the loading seqquence.

##### Fixed parameters
The period of the independent sinusoidal lattices are fixed. The long lattice period is 1.5um and the short lattice period is 0.5um. 
The sinusoidal lattices are approximated by series of connected Gaussians. It is a reasonable approach, for the arguments please checkout 
* https://math.stackexchange.com/questions/1346627/is-it-possible-to-approximate-cosx-with-a-linear-combination-of-gaussians
* https://math.stackexchange.com/questions/2447462/approximation-of-the-cosine-by-gaussian-functions?newreg=36d679214c8445e291cddb1f0348f085



#### Name
##### _PatternedLoader(qmf).prepare_matter(name)_
#### Usage
This function returns as completely prepared quantum matter object, which can be directly submitted to the Oqtant service.

Even with no superlattice specified, the matter has default zero settings:
* All potentials and periods are zero
* All loading sequence delays, edges and holds are zero
* The job duration is still the default 6ms.

That is, even with no settings the job is a default matter with IN TRAP duration of 6ms.

### Usage Example

    ```python
    qmf = QuantumMatterFactory()
    qmf.get_login()

    pl = PatternedLoader(qmf. "Expt1Matter")

    short = pl.Lattice()
    short.set_potential(pot)
    short.set_loading_seq(delay, edge, hold)

    long = pl.Lattice()
    long.set_potential(pot)
    long.set_loading_seq(delay, edge, hold)

    pl.set_superlattice(long, short)

    matter = pl.get_matter()

    matter.submit(sim=True)
    ```
