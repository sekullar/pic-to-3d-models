#!/usr/bin/env python3
"""
Fotoğraftan 3D Obje Üretici (Hunyuan3D-2 tabanlı)
===================================================

*** BU SCRIPT SADECE Hunyuan3D-2 İÇİNDİR ***


Klasör yapısı:
    input/<KisiAdi>/foto.jpg   ->   output/<KisiAdi>/model.glb

Kurallar:
- input/ ve output/ klasörleri yoksa otomatik oluşturulur.
- Her kişi klasöründe birden fazla fotoğraf varsa SADECE ilk fotoğraf işlenir.
- İşlenen fotoğraf, tekrar işlenmemesi için "<isim>_old.<uzanti>" olarak yeniden adlandırılır.
- GPU (CUDA) varsa otomatik kullanılır, yoksa CPU'ya düşülür (Hunyuan3D-2 CPU'da ÇOK yavaş olur).
- Model ağırlıkları Hugging Face üzerinden ilk çalıştırmada otomatik indirilip
  yerel cache'e kaydedilir, sonraki çalıştırmalarda tekrar indirilmez.

Kurulum (bir kere yapılır):
    !bash setup_hunyuan.sh

Çalıştırma:
    !python photo_to_3d_hunyuan.py
"""

import os
import sys
import logging
import argparse
from pathlib import Path

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
log = logging.getLogger("photo3d_hunyuan")

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
HUNYUAN_REPO_DIR = BASE_DIR / "Hunyuan3D2_repo"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

# Varsayılanlar (disk/VRAM dostu: mini + turbo shape modeli)
DEFAULT_SHAPE_MODEL_ID = "tencent/Hunyuan3D-2mini"
DEFAULT_SHAPE_SUBFOLDER = "hunyuan3d-dit-v2-mini-turbo"
DEFAULT_TEXTURE_MODEL_ID = "tencent/Hunyuan3D-2"
DEFAULT_TEXTURE_SUBFOLDER = None  # None = kütüphanenin kendi varsayılanı


# --------------------------------------------------------------------------- #
# Klasör kontrolleri
# --------------------------------------------------------------------------- #
def ensure_folders():
    for d in (INPUT_DIR, OUTPUT_DIR):
        if d.exists():
            log.info(f"'{d.name}/' klasörü mevcut, sorun yok.")
        else:
            log.info(f"'{d.name}/' klasörü bulunamadı, oluşturuluyor: {d}")
            d.mkdir(parents=True, exist_ok=True)


def check_hunyuan_installed() -> bool:
    """hy3dgen paketinin (Hunyuan3D-2 kütüphanesi) kurulu olup olmadığını kontrol eder."""
    try:
        import hy3dgen  # noqa: F401
        return True
    except ImportError:
        if HUNYUAN_REPO_DIR.exists() and str(HUNYUAN_REPO_DIR) not in sys.path:
            sys.path.insert(0, str(HUNYUAN_REPO_DIR))
            try:
                import hy3dgen  # noqa: F401
                return True
            except ImportError:
                return False
        return False


def prompt_setup_instructions():
    log.error("hy3dgen (Hunyuan3D-2) kütüphanesi bulunamadı!")
    log.error("Lütfen önce kurulumu tamamlayın, sonra scripti tekrar çalıştırın:")
    log.error(f"    bash {BASE_DIR / 'setup_hunyuan.sh'}")
    sys.exit(1)


# --------------------------------------------------------------------------- #
# Model yolu doğrulama
# --------------------------------------------------------------------------- #
def _is_valid_hf_repo(repo_id: str) -> bool:
    try:
        from huggingface_hub import HfApi
        HfApi().model_info(repo_id)
        return True
    except Exception:
        return False


def resolve_model_config(cli_shape_model, cli_shape_subfolder, cli_texture_model,
                          cli_texture_subfolder, cli_skip_texture):
    """
    Shape (geometri) ve texture (renklendirme) modelleri için repo ID / yerel yol
    ve subfolder bilgisini belirler. CLI parametreleri verilmişse direkt onları
    kullanır (sorulmaz), verilmemişse interaktif olarak sorulur.
    """
    def _check_repo_or_path(value: str, label: str):
        candidate = Path(value).expanduser()
        if candidate.exists():
            log.info(f"{label}: yerel yol kullanılacak -> {candidate}")
            return str(candidate)
        if _is_valid_hf_repo(value):
            log.info(f"{label}: Hugging Face repo doğrulandı -> {value}")
            return value
        log.warning(
            f"'{value}' ne geçerli bir yerel yol ne de erişilebilir bir "
            f"Hugging Face repo ({label}). Tekrar deneyin."
        )
        return None

    # --- Shape model ---
    if cli_shape_model:
        shape_model = _check_repo_or_path(cli_shape_model, "Shape model")
        if shape_model is None:
            log.error("--shape-model ile verilen değer doğrulanamadı. Script durduruluyor.")
            sys.exit(1)
    else:
        while True:
            user_input = input(
                f"Shape (geometri) model yolu/ID [Enter = varsayılan "
                f"'{DEFAULT_SHAPE_MODEL_ID}']: "
            ).strip()
            value = user_input if user_input else DEFAULT_SHAPE_MODEL_ID
            shape_model = _check_repo_or_path(value, "Shape model")
            if shape_model:
                break

    if cli_shape_subfolder is not None:
        shape_subfolder = cli_shape_subfolder
    else:
        user_input = input(
            f"Shape model subfolder [Enter = varsayılan '{DEFAULT_SHAPE_SUBFOLDER}']: "
        ).strip()
        shape_subfolder = user_input if user_input else DEFAULT_SHAPE_SUBFOLDER

    # --- Texture model (opsiyonel) ---
    skip_texture = cli_skip_texture
    texture_model = None
    texture_subfolder = None

    if not skip_texture:
        if cli_texture_model:
            texture_model = _check_repo_or_path(cli_texture_model, "Texture model")
            if texture_model is None:
                log.error("--texture-model ile verilen değer doğrulanamadı. Script durduruluyor.")
                sys.exit(1)
        else:
            answer = input(
                "Texture (renklendirme) modeli de kullanılsın mı? "
                "Bu, VRAM/disk kullanımını belirgin artırır (evet/hayır) "
                "[Enter = evet]: "
            ).strip().lower()
            if answer in ("hayır", "hayir", "no", "n", "h"):
                skip_texture = True
            else:
                while True:
                    user_input = input(
                        f"Texture model yolu/ID [Enter = varsayılan "
                        f"'{DEFAULT_TEXTURE_MODEL_ID}']: "
                    ).strip()
                    value = user_input if user_input else DEFAULT_TEXTURE_MODEL_ID
                    texture_model = _check_repo_or_path(value, "Texture model")
                    if texture_model:
                        break
                texture_subfolder = cli_texture_subfolder  # None ise kütüphane varsayılanı kullanılır

    if skip_texture:
        log.info("Texture adımı ATLANACAK: sadece geometri (renksiz/vertex-color olmayan mesh) üretilecek.")

    return {
        "shape_model": shape_model,
        "shape_subfolder": shape_subfolder,
        "texture_model": texture_model,
        "texture_subfolder": texture_subfolder,
        "skip_texture": skip_texture,
    }


def print_usage_instructions():
    log.info("")
    log.info("=" * 70)
    log.info("Dönüştürmek istediğiniz fotoğrafları 'input/' klasörünün içine,")
    log.info("HER FOTOĞRAF İÇİN AYRI YENİ BİR KLASÖR açarak koyun. Örnek:")
    log.info("    input/Ahmet/foto.jpg")
    log.info("    input/Mehmet/foto.jpg")
    log.info("")
    log.info("İşlem bittikten sonra input/ ve output/ klasörlerindeki dosyaları")
    log.info("SİLMENİZE GEREK YOKTUR: işlenen fotoğraflar '_old' etiketiyle")
    log.info("işaretlenir ve bir sonraki çalıştırmada tekrar işlenmez.")
    log.info("=" * 70)
    log.info("")


# --------------------------------------------------------------------------- #
# Kişi klasörlerini / fotoğrafları bulma (TripoSR script'iyle aynı mantık)
# --------------------------------------------------------------------------- #
def find_person_folders():
    return sorted([p for p in INPUT_DIR.iterdir() if p.is_dir()])


def find_unprocessed_image(person_folder: Path):
    candidates = sorted(
        f
        for f in person_folder.iterdir()
        if f.is_file()
        and f.suffix.lower() in IMAGE_EXTENSIONS
        and not f.stem.endswith("_old")
    )
    return candidates[0] if candidates else None


def mark_as_processed(image_path: Path):
    new_name = image_path.with_name(f"{image_path.stem}_old{image_path.suffix}")
    counter = 1
    while new_name.exists():
        new_name = image_path.with_name(
            f"{image_path.stem}_old_{counter}{image_path.suffix}"
        )
        counter += 1
    image_path.rename(new_name)
    log.info(f"İşlenen fotoğraf işaretlendi: {image_path.name} -> {new_name.name}")


# --------------------------------------------------------------------------- #
# Model yükleme (Hunyuan3D-2 resmi API'sine göre)
# --------------------------------------------------------------------------- #
def load_pipelines(config: dict, device_preference="auto"):
    import torch
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

    if device_preference == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = device_preference
        if device.startswith("cuda") and not torch.cuda.is_available():
            log.warning("CUDA istendi ama bulunamadı, CPU'ya düşülüyor.")
            device = "cpu"

    if device == "cpu":
        log.warning(
            "GPU bulunamadı: Hunyuan3D-2 CPU'da ÇOK yavaş çalışır (muhtemelen "
            "onlarca dakika/fotoğraf). Mümkünse GPU'lu bir ortam (Colab GPU) kullanın."
        )

    log.info(f"Cihaz: {device}")
    log.info(
        f"Shape modeli yükleniyor: '{config['shape_model']}' "
        f"(subfolder: {config['shape_subfolder']})"
    )
    shape_kwargs = {}
    if config["shape_subfolder"]:
        shape_kwargs["subfolder"] = config["shape_subfolder"]
    shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
        config["shape_model"], **shape_kwargs
    )
    shape_pipeline.to(device)

    texture_pipeline = None
    if not config["skip_texture"]:
        from hy3dgen.texgen import Hunyuan3DPaintPipeline

        log.info(f"Texture modeli yükleniyor: '{config['texture_model']}'")
        texture_kwargs = {}
        if config["texture_subfolder"]:
            texture_kwargs["subfolder"] = config["texture_subfolder"]
        texture_pipeline = Hunyuan3DPaintPipeline.from_pretrained(
            config["texture_model"], **texture_kwargs
        )

    log.info("Model(ler) başarıyla yüklendi.")
    return shape_pipeline, texture_pipeline, device


# --------------------------------------------------------------------------- #
# Tek bir fotoğrafı 3D objeye çevirme
# --------------------------------------------------------------------------- #
def process_image(shape_pipeline, texture_pipeline, image_path: Path, output_folder: Path):
    import torch
    from PIL import Image
    from hy3dgen.rembg import BackgroundRemover

    output_folder.mkdir(parents=True, exist_ok=True)

    log.info(f"Fotoğraf işleniyor: {image_path}")

    image = Image.open(image_path).convert("RGBA")
    # Arka planı temizle (RGB gelirse rembg ile alfa kanalı ekle)
    if image.mode != "RGBA" or image.getchannel("A").getextrema() == (255, 255):
        rembg = BackgroundRemover()
        image = rembg(image)

    try:
        mesh = shape_pipeline(image=image)[0]
    except torch.cuda.OutOfMemoryError:
        log.error(
            "GPU belleği yetersiz (OOM) - shape üretimi sırasında. Daha küçük bir "
            "shape modeli (mini/mini-turbo) kullanmayı deneyin."
        )
        raise

    if texture_pipeline is not None:
        try:
            mesh = texture_pipeline(mesh, image=image)
        except torch.cuda.OutOfMemoryError:
            log.error(
                "GPU belleği yetersiz (OOM) - texture üretimi sırasında. "
                "Texture adımını atlamak için --skip-texture parametresini kullanabilirsiniz."
            )
            raise

    out_mesh_path = output_folder / "model.glb"
    mesh.export(str(out_mesh_path))
    log.info(f"3D obje kaydedildi: {out_mesh_path}")
    return out_mesh_path


# --------------------------------------------------------------------------- #
# Ana akış
# --------------------------------------------------------------------------- #
def main():
    parser = argparse.ArgumentParser(
        description="Fotoğraftan 3D obje üretici (Hunyuan3D-2) - "
        "TripoSR için bu script değil, 'photo_to_3d.py' kullanılmalı."
    )
    parser.add_argument("--device", default="auto", help="'auto' (varsayılan), 'cuda' veya 'cpu'")
    parser.add_argument("--shape-model", default=None, help="Shape model yolu/HF ID'si")
    parser.add_argument("--shape-subfolder", default=None, help="Shape model subfolder adı")
    parser.add_argument("--texture-model", default=None, help="Texture model yolu/HF ID'si")
    parser.add_argument("--texture-subfolder", default=None, help="Texture model subfolder adı")
    parser.add_argument(
        "--skip-texture",
        action="store_true",
        help="Texture üretimini tamamen atla (sadece geometri üret, VRAM/disk tasarrufu)",
    )
    args = parser.parse_args()

    log.info("*** Bu script Hunyuan3D-2 içindir. TripoSR kullanacaksanız "
              "'photo_to_3d.py' dosyasını kullanın. ***")

    ensure_folders()

    if not check_hunyuan_installed():
        prompt_setup_instructions()

    config = resolve_model_config(
        args.shape_model, args.shape_subfolder,
        args.texture_model, args.texture_subfolder,
        args.skip_texture,
    )
    print_usage_instructions()

    person_folders = find_person_folders()
    if not person_folders:
        log.info("input/ klasörü altında henüz kişi klasörü yok. Eklendiğinde tekrar çalıştırın.")
        return

    pending = []
    for person_folder in person_folders:
        image_path = find_unprocessed_image(person_folder)
        if image_path:
            pending.append((person_folder, image_path))
        else:
            log.info(f"'{person_folder.name}' için yeni/işlenmemiş fotoğraf yok, atlanıyor.")

    if not pending:
        log.info("İşlenecek yeni fotoğraf bulunamadı. Herkes güncel.")
        return

    shape_pipeline, texture_pipeline, device = load_pipelines(config, device_preference=args.device)

    for person_folder, image_path in pending:
        output_folder = OUTPUT_DIR / person_folder.name
        try:
            process_image(shape_pipeline, texture_pipeline, image_path, output_folder)
            mark_as_processed(image_path)
        except Exception as e:
            log.error(f"'{person_folder.name}' işlenirken hata oluştu: {e}")
            log.error("Bu kişi atlanıyor, fotoğrafı '_old' olarak işaretlenmedi.")

    log.info("Tüm işlemler tamamlandı.")


if __name__ == "__main__":
    main()
