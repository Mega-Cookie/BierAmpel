#!/bin/sh
set -e
case "$1" in
    remove|upgrade|deconfigure)
        echo "Stoppe BierAmpel Service..."
        systemctl stop BierAmpel || true
        ;;
    *)
        echo "prerm aufgerufen mit unbekanntem Argument '$1'" >&2
        exit 1
        ;;
esac
exit 0