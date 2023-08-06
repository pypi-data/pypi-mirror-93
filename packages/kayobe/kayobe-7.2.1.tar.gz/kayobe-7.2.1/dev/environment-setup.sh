#!/bin/bash

# Save the current shell options.
oldstate=$(set +o)

set -eu
set -o pipefail

# This script can be used to prepare the environment for use with kayobe. This
# includes setting environment variables and activating the python virtual
# environment. This script should be sourced rather than executed in a
# subprocess. e.g. source dev/environment-setup.sh

PARENT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "${PARENT}/functions"


function main {
    config_init
    environment_setup
}

main

# Restore previous shell options.
eval "$oldstate"
