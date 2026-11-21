#!/bin/sh
# Instala (o actualiza) el juez como servicio systemd en la Raspberry Pi.
# Uso, desde esta carpeta:   sh instalar.sh            (pide sudo)
# Usa el usuario actual y la copia del repo DA en la que está este archivo.
set -eu
AQUI=$(cd "$(dirname "$0")" && pwd)
CARPETA=$(cd "$AQUI/../.." && pwd)
USUARIO=$(id -un)

echo "== Dependencias"
falta=""
for p in python3 g++ bwrap prlimit; do command -v "$p" >/dev/null || falta="$falta $p"; done
if [ -n "$falta" ]; then
  echo "Faltan:$falta -> sudo apt install -y python3 g++ bubblewrap util-linux"
  sudo apt-get install -y python3 g++ bubblewrap util-linux
fi

echo "== Diagnóstico (antes de instalar)"
if ! python3 "$AQUI/servidor.py" --diagnostico; then
  echo "La autoprueba falla: revisa el mensaje de arriba antes de seguir." >&2
  exit 1
fi

echo "== Servicio"
sed -e "s#USUARIO#$USUARIO#g" -e "s#CARPETA#$CARPETA#g" "$AQUI/juez-da.service" | sudo tee /etc/systemd/system/juez-da.service >/dev/null
sudo systemctl daemon-reload
sudo systemctl enable juez-da >/dev/null
sudo systemctl restart juez-da
sleep 6
systemctl --no-pager --lines=8 status juez-da || true
echo
echo "== Salud"
curl -s "http://127.0.0.1:${JUEZ_PUERTO:-8099}/salud/sistema" || echo "no responde (mira: journalctl -u juez-da -n 50)"
echo
echo "Listo. Prueba completa:  python3 $AQUI/probar.py"
