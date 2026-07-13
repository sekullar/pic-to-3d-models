#!/usr/bin/env bash
# Hunyuan3D-2 kurulum scripti (Colab veya yerel için)
# Bu scripti sadece BİR KERE çalıştırman yeterli.
#
# LİSANS NOTU: Hunyuan3D-2, Tencent Hunyuan Non-Commercial License altındadır.
# Ticari kullanım için repo'daki lisans metnini kontrol et.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$SCRIPT_DIR/Hunyuan3D2_repo"

echo "==> Hunyuan3D-2 kurulumu başlıyor..."

if [ -d "$REPO_DIR" ]; then
    echo "Hunyuan3D2_repo klasörü zaten mevcut, indirme atlanıyor."
else
    echo "Hunyuan3D-2 reposu indiriliyor..."
    git clone --depth 1 https://github.com/Tencent/Hunyuan3D-2.git "$REPO_DIR"
fi

echo "==> Python bağımlılıkları kuruluyor..."
pip install -r "$REPO_DIR/requirements.txt"

echo "==> hy3dgen paketi kuruluyor..."
cd "$REPO_DIR"
pip install -e .

echo "==> Texture (custom_rasterizer) modülü derleniyor..."
cd "$REPO_DIR/hy3dgen/texgen/custom_rasterizer"
python3 setup.py install

echo "==> Texture (differentiable_renderer) modülü derleniyor..."
cd "$REPO_DIR/hy3dgen/texgen/differentiable_renderer"
python3 setup.py install

cd "$SCRIPT_DIR"

echo ""
echo "==> Kurulum tamamlandı!"
echo ""
echo "NOT: PyTorch'un CUDA sürümünün ayrıca kurulu olduğundan emin ol:"
echo "    https://pytorch.org/get-started/locally/"
echo ""
echo "Şimdi 'input/<KisiAdi>/foto.jpg' şeklinde fotoğraf ekleyip"
echo "'python photo_to_3d_hunyuan.py' komutunu çalıştırabilirsin."
