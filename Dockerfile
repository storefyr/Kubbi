# Sailfish OS Platform SDK image for building the VoxeLibre RPMs.
#
#   docker build -t kubbi-sailfish-sdk .
#   docker run --rm -v "$PWD":/home/mersdk/kubbi -w /home/mersdk/kubbi \
#       kubbi-sailfish-sdk sh tools/build-rpms.sh
#
# Resulting RPMs land in ./RPMS inside the repository checkout.
FROM ghcr.io/sailfishos-open/docker-sailfishos-builder-aarch64:5.1.0.11

USER root
RUN zypper --non-interactive refresh || true
USER mersdk

WORKDIR /home/mersdk
