# Verification environment for track B (kernel build + QEMU boot).
# Mirrors the CI toolchain (Ubuntu + GCC + QEMU + Limine) so B07+ can be
# compiled and booted locally before any PASS is claimed. Built for the
# host arch; an x86_64-elf cross toolchain produces the freestanding ELF and
# qemu-system-x86_64 runs it under TCG.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc-x86-64-linux-gnu \
        binutils-x86-64-linux-gnu \
        build-essential \
        qemu-system-x86 \
        xorriso \
        mtools \
        curl \
        ca-certificates \
        git \
        python3 \
    && rm -rf /var/lib/apt/lists/*

# Limine protocol header (for the build) and binary release (for the boot ISO).
RUN curl --fail --location --retry 3 \
        --output /opt/limine.h \
        https://raw.githubusercontent.com/limine-bootloader/limine-protocol/trunk/include/limine.h \
    && test -s /opt/limine.h
RUN git clone --depth 1 --branch v9.x-binary \
        https://github.com/limine-bootloader/limine.git /opt/limine \
    && make -C /opt/limine \
    && test -x /opt/limine/limine

ENV LIMINE_HEADER=/opt/limine.h
ENV LIMINE_DIR=/opt/limine
ENV CC=x86_64-linux-gnu-gcc
ENV LD=x86_64-linux-gnu-ld
ENV READELF=x86_64-linux-gnu-readelf

WORKDIR /work
