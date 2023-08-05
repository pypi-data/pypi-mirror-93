# Pinttrs

*Pint meets attrs*

[![Documentation Status](https://readthedocs.org/projects/pinttrs/badge/?version=latest)](https://pinttrs.readthedocs.io/en/latest/?badge=latest)

## Motivation

The amazing [`attrs`](https://www.attrs.org) library is a game-changer when it 
comes to writing classes. Its initialisation sequence notably allows for 
automated conversion and verification of attribute values. This package is an 
attempt at designing a system to apply units automatically and reliably to 
attributes with [Pint](https://pint.readthedocs.io).

## Features

- [x] Automatic attachment of predefined units to unitless values
- [x] Verification of units compatibility for Pint quantity values
- [x] Interpretation of units in dictionaries
- [ ] Dynamic fetching of units from a registry

## License

Pinttrs is distributed under the terms of the 
[MIT license](https://choosealicense.com/licenses/mit/).

## About

Pinttrs is written and maintained by [Vincent Leroy](https://github.com/leroyvn).

The development is supported by [Rayference](https://www.rayference.eu).

Pinttrs is a component of the 
[Eradiate radiative transfer model](https://www.eradiate.eu).

The Pinttrs logo is based on 
[Agus Nugroho](https://www.iconfinder.com/nugrohoagus)'s glass icon and parts of 
the ``attrs`` logo.
