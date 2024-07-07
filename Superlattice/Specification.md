# Patterned Loading Requirements Specification 
This feature creates a superlattice potential over a BEC. Two independent lattices are applied in sequence over the BEC. Depending on the potentials and periods of the lattices, the BEC atoms can be selectively loaded or confined to some sites, and removed in others. This technique is referred to as Patterned Loading.
## Outline
* Features
* API
    * Function Name
    * Usage
* Usage Example

### Features


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
    short.set_loading_seq(delay, rising_edge, hold, falling_edge)

    long = pl.Lattice()
    long.set_potential(pot, period)
    long.set_loading_seq(delay, rising_edge, hold, falling_edge)

    pl.set_lattice(long, short)

    matter = pl.get_matter()

    matter.submit(sim=True)
    ```
