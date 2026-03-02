# Ambilight

A lightweight Python project that interfaces with Hyperion to provide an ambient lighting experience.
Includes a Rust-based listener component (`hyperion_rust`) for high-performance communication with Hyperion's backend.

## Overview

This repository contains:

- `main.py`: Hyperion UDP paquet listener that controls the GPIO for LED operation.
- `test.py`: Hyperion UDP paquet listener that prints the received paquets to stdout.
- `hyperion_rust/`: a Rust listener for higher performance (WiP).

## Usage

Activate the virtual environment and run `python main.py` to start the ambilight service.

## Development

See `pyproject.toml` for Python dependencies and use `cargo` within `hyperion_rust/` for Rust builds.
