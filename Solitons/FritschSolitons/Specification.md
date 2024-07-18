# Fritsch Solitons Requirements Specification

What I am calling the Fritsch method is a way to create dark solitons at arbitrary position and velocity by simultaneously engineering the amplitude and phase of the condensate wave function. This is supposed to be a better approach compared to the technique we demonstrated before which manipulated the condensate phase only.

* Fritsch, A.R., Lu, M., Reid, G., Piñeiro, A., & Spielman, I.B. (2020). Creating solitons with controllable and near-zero velocity in Bose-Einstein condensates. Physical review. A, 101 5.

Date: 2024/04/18

Author: Joshua D. JOHN

## Outline
* Features
* API
    * Function Name
    * Usage
* Usage Examples

## Features

## API

## Usage Examples
```python
    qmf = QuantumMatterFactory()
    qmf.get_login()

    fs = FristchSoliton(qmf)

    phi = 1 # in pi units
    fs.set_imprinting_phase(phi)

    matter = ps.get_matter()

    matter.submit(sim=True)
    ```