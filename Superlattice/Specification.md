# Patterned Loading Requirements Specification 
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
