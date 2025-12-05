#!/bin/bash
DJANGO_ROOT="eg0n_portal"

# Alpine.js: https://www.jsdelivr.com/package/npm/alpinejs
ALPINEJS_VERSION="3.15.0"
ALPINEJS_CDN_URL="https://cdn.jsdelivr.net/npm/alpinejs@${ALPINEJS_VERSION}/dist"
wget -q -O- "${ALPINEJS_CDN_URL}/cdn.min.js" > ${DJANGO_ROOT}/static/alpinejs/js/alpinejs.min.js
wget -q -O- "${ALPINEJS_CDN_URL}/cdn.min.js.map" > ${DJANGO_ROOT}/static/alpinejs/js/alpinejs.min.js.map

# Tabler: https://www.jsdelivr.com/package/npm/@tabler/core
TABLER_VERSION="1.4.0"
TABLER_CDN_URL="https://cdn.jsdelivr.net/npm/@tabler/core@${TABLER_VERSION}/dist"
wget -q -O- "${TABLER_CDN_URL}/js/tabler.min.js" > ${DJANGO_ROOT}/static/tabler/js/tabler.min.js
wget -q -O- "${TABLER_CDN_URL}/js/tabler.min.js.map" > ${DJANGO_ROOT}/static/tabler/js/tabler.min.js.map
wget -q -O- "${TABLER_CDN_URL}/css/tabler.min.css" > ${DJANGO_ROOT}/static/tabler/css/tabler.min.css
wget -q -O- "${TABLER_CDN_URL}/css/tabler.min.css.map" > ${DJANGO_ROOT}/static/tabler/css/tabler.min.css.map

# UI
rsync -a --exclude __pycache__ ../unetlab/unetlab/ui/ eg0n_portal/ui/
rsync -a --exclude __pycache__ ../unetlab/unetlab/templates/ui/ eg0n_portal/_templates/ui/
rsync -a --exclude __pycache__ ../unetlab/unetlab/static/ui/ eg0n_portal/static/ui/
rsync -a --exclude __pycache__ ../unetlab/unetlab/tests/ui/ eg0n_portal/tests/ui/
