daml-dit-api
====

API definitions for integrations and other sorts of packages to be
hosted by DABL. This contains the following:

* [The definition for the package metadata format](daml_dit_api/package_metadata.py)
* [The call API for integration bots](daml_dit_api/integration_api.py)

# Package Metadata

At their core, DIT files are [ZIP archives](https://en.wikipedia.org/wiki/Zip_(file_format))
that follow a specific set of conventions regarding their content. The
most important of these conventions is the presence of a YAML metadata
file at the root of the archive and named `dabl-meta.yaml`. This
metadata file contains catalog information describing the contents of
the DIT, as well as any packaging details needed to successfully
deploy a DIT file into DABL. An example of a deployment instruction is
a _subdeployment_. A subdeployment instructs DABL to deploy a specific
subfile within the DIT file. A DIT file that contains an embedded DAR
file could use a subdeployment to ensure that the embedded DAR file is
deployed to the ledger when the DIT is deployed. In this way, a DIT
file composed of multiple artifacts (DARs, Bots, UI's, etc.) can be
constructed to deploy a set of artifacts to a single ledger in a
single action.

# Integrations

Integrations are a special case of DIT file that are augmented with
the ability to run as an executable within a DABL cluster. This is
done by packaging Python [DAZL bot](https://github.com/DACH-NY/dazl)
code into an [executable ZIP](https://docs.python.org/3/library/zipapp.html)
using [PEX](https://github.com/pantsbuild/pex) and augmenting tha
resulting file with the metadata and other resources needed to make it
a correctly formed DIT file.

Logically speaking, DABL integrations are DAZL bots packaged with
information needed to fit them into the DABL runtime and user
interface. The major functional contrast between a DABL integration
and a Python Bot is that the integration has the external network
access needed to connect to an outside system and the Python Bot does
not. Due to the security implications of running within DABL with
external network access, integrations can only be deployed with the
approval of DA staff.

## Developing Integrations

The easiest way to develop an integration for DABL is to use the
[framework library](https://github.com/digital-asset/daml-dit-integration-framework)
and [`ddit` build tool](https://github.com/digital-asset/daml-dit-ddit).
The integration framework presents a Python API closely related to the
DAZL bot api and ensures that integrations follow the conventions
required to integrate into DABL. The framework parses ledger
connection arguments, translates configuration metadata into a domain
object specific to the integration, and exposes the appropriate health
check endpoints required to populate the DABL integration user
interface.

_Unless you know exactly what you are doing and why you are doing it,
use the framework._

### The Integration Runtime Environment

By convention, integrations accept a number of environment variables
that specify key paramaters.  Integrations built with the framework
use defaults for these variables that connect to a default locally
configured sandbox instance.

Available variables include the following:

| Variable | Default | Purpose |
|----------|---------|---------|
| `DABL_HEALTH_PORT` | 8089 | Port for Health/Status HTTP endpoint |
| `DABL_INTEGRATION_METADATA_PATH` | 'int_args.yaml' | Path to local metadata file |
| `DABL_INTEGRATION_TYPE_ID` | | Type ID for the specific integration within the DIT to run |
| `DABL_LEDGER_ID` | 'cloudbox' | Ledger ID for local ledger |
| `DABL_LEDGER_URL` | `http://localhost:6865` | Address of local ledger gRPC API |
