#!/bin/sh
set -e
case "$1" in
    configure)
        echo "Aktualisiere Systemd Daemon und starte BierAmpel Service..."
        systemctl daemon-reload
        systemctl enable BierAmpel
        systemctl start BierAmpel
        ;;
    *)
        echo "postinst aufgerufen mit unbekanntem Argument '$1'" >&2
        exit 1
        ;;
esac
exit 0