# Patterned Loading Requirements Specification 
This feature creates a superlattice potential over a BEC. Two independent lattices are applied in sequence over the BEC. Depending on the potentials and periods of the lattices, the BEC atoms can be selectively loaded or confined to some sites, and removed in others. This technique is referred to as Patterned Loading.
## Outline
* Features
* API
    * Function Name
    * Usage
* Usage Example

### Features
* Creates a job that can be submitted to the Oqtant Quantum Matter Service. This job is a completeley prepared quantum matter with its landscapes, snapshots and lasers already set.
* Provides a way to set the potential profile for the superlattice of two independent sinusoidal lattices.
* Provides a way to prepare a general sinusoidal lattice specified by its potential amplitude and period.
* Provides a way to prepare a loading sequence for each independent lattice. The loading sequence is specified by a "gaussian" pulse with parameters of delay, edge "sharpness" and hold.
* An internal algorithm uses the specified two independent lattices to prepare quantum matter landscapes, snapshots and lasers and produce a submittable job.

### API
#### Name
#### Usage

### Usage Example

    ```python
    qmf = QuantumMatterFactory()
    qmf.get_login()

    pl = PatternedLoader(qmf)

    short = pl.Lattice()
    short.set_potential(pot, period)
    short.set_loading_seq(delay, edge, hold)

    long = pl.Lattice()
    long.set_potential(pot, period)
    long.set_loading_seq(delay, edge, hold,)

    pl.set_lattice(long, short)

    matter = pl.get_matter()

    matter.submit(sim=True)
    ```
