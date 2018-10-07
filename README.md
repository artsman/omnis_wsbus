# OMNIS WebSocket Bus

A simple websocket relay for use with Omnis OW3 HTTP Workers with
Web Socket support.

## Requirements

Python 3.6+ (All Platforms)

## Omnis Studio Demo Requirements

Omnis Studio 8.1.6+

## Getting started

Install dependencies: `pip install -r requirements.txt`

Run CLI: `python manage.py`

Build binary: `pyinstaller omnis_wsbus.spec`

Run Omnis Demo: Open Omnis Studio and import `omnis-wsbus-demo`


## Omnis Demo Library

An Omnis demo library is included in JSON format.  It can be used as a
reference of a simple WebSocket implementation.  It can also be used
to test connections.


## Self-signed SSL Certificates

There are two shell scripts, `build_ca_cert` and
`build_self_cert`, and one configuration file, `self_cert.cnf` that
simplify the creation of custom root and self-signed SSL certicates.

A pre-built self-signed root and certificate is included in the
binaries for convenience.  It can be dumped out of the binary
with `./omnis_wsbus certs /path/to/dump`.
