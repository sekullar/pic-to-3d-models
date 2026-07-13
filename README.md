# 🖼️➡️🧊 pic-to-3d-models

## Convert Images to 3D Models with AI

Generate high-quality 3D meshes from images using **Hunyuan3D**.

> ⚠️ This project currently works **only on Google Colab**.

---

# 🚀 Getting Started

## 1️⃣ Requirements

Before running the project:

- Use **Google Colab**
- Set **Runtime → T4 GPU**

> **Important:**  
> If you don't select **T4 GPU**, the setup script may fail.

---

## 2️⃣ Installation

Upload the project files to your Colab workspace and run:

```bash
!bash setup_hunyuan.sh
```

This command only needs to be executed **once per Colab session**.

Wait until the installation finishes before continuing.

---

## 3️⃣ Preparing Images

Create an `input` directory.

```text
input/
```

Each image must be placed inside its **own folder**.

Example:

```text
input/
├── car/
│   └── car.png
├── character/
│   └── character.jpg
└── house/
    └── house.jpeg
```

Each folder is processed as an independent project.

Generated models will be saved to:

```text
output/
```

---

## 4️⃣ Run

Execute:

```bash
!python photo_to_3d_hunyuan.py
```

Alternative API support is currently limited, so you can usually keep every prompt at its **default value**.

---

# 🎨 Texture Generation (Optional)

By default, this project generates **only the 3D mesh**.

If you also want textures, install the **Hunyuan3D Paint** model in your Colab environment.

When prompted, simply provide the model path.

---

# 📂 Output

```text
output/
├── project_1/
├── project_2/
└── ...
```

Each project will contain its own generated 3D model.

---

# 📌 Notes

- Local execution is **not supported yet**.
- Future updates may include support for local AI models and APIs.

---

---

# 🤖 Compatible Shape Models (Google Colab)

The following **Hunyuan3D Shape models** have been tested and are compatible with this script when running in **Google Colab**.

| Repository | Subfolder | Size | Description |
|------------|-----------|------|-------------|
| `tencent/Hunyuan3D-2mini` | `hunyuan3d-dit-v2-mini` | 0.6B | Standard Mini model. Fast and lightweight. |
| `tencent/Hunyuan3D-2mini` | `hunyuan3d-dit-v2-mini-turbo` | 0.6B | **Recommended.** Fastest model with excellent generation speed. |
| `tencent/Hunyuan3D-2mini` | `hunyuan3d-dit-v2-mini-fast` | 0.6B | Alternative distilled Mini model optimized for speed. |
| `tencent/Hunyuan3D-2` | `hunyuan3d-dit-v2-0` | 1.1B | Higher-quality base model. Slower but produces better results. |
| `tencent/Hunyuan3D-2` | `hunyuan3d-dit-v2-0-turbo` | 1.1B | Faster version of the base model. |
| `tencent/Hunyuan3D-2` | `hunyuan3d-dit-v2-0-fast` | 1.1B | Alternative speed-optimized version of the base model. |
| `tencent/Hunyuan3D-2mv` | `hunyuan3d-dit-v2-mv`, `-turbo`, `-fast` | 1.1B | Multi-view models designed for multiple input images. |
| `tencent/Hunyuan3D-2.1` | `hunyuan3d-dit-v2-1` | 3.0B | Latest and largest generation (June 2025). May require significantly more VRAM. |

> 💡 **Recommendation:**  
> For Google Colab **T4 GPU**, `hunyuan3d-dit-v2-mini-turbo` provides the best balance between speed and quality.

---

> 💙 **Friendly Recommendation:**  
> If you're using the **free Google Colab** plan, **Hunyuan3D-2mini** and especially **Hunyuan3D-2mini Turbo** are recommended. They offer the best balance between generation speed, quality, and available GPU resources.

---


# ⭐ Credits

Developed by **Seku** with AI Assistance.

Made with ❤️ and a little artificial intelligence.

---

# 🇹🇷 Türkçe

## Yapay Zeka ile Görselleri 3D Modele Dönüştürün

Bu proje, **Hunyuan3D** kullanarak görsellerden yüksek kaliteli 3D mesh modeller üretir.

> ⚠️ Proje şu anda **yalnızca Google Colab** üzerinde çalışmaktadır.

---

# 🚀 Başlangıç

## 1️⃣ Gereksinimler

Projeyi çalıştırmadan önce:

- **Google Colab** kullanın.
- **Runtime → T4 GPU** seçin.

> **Önemli:**  
> **T4 GPU** seçmezseniz kurulum scripti başarısız olabilir.

---

## 2️⃣ Kurulum

Proje dosyalarını Colab ortamına yükledikten sonra aşağıdaki komutu çalıştırın:

```bash
!bash setup_hunyuan.sh
```

Bu komutu **her Colab oturumunda yalnızca bir kez** çalıştırmanız yeterlidir.

Kurulum tamamlandıktan sonra bir sonraki adıma geçebilirsiniz.

---

## 3️⃣ Görselleri Hazırlama

`input` adlı bir klasör oluşturun.

```text
input/
```

Her görsel **kendine ait ayrı bir klasörde** bulunmalıdır.

Örnek:

```text
input/
├── car/
│   └── car.png
├── character/
│   └── character.jpg
└── house/
    └── house.jpeg
```

Her klasör bağımsız bir proje olarak işlenir.

Oluşturulan modeller:

```text
output/
```

klasörüne kaydedilir.

---

## 4️⃣ Çalıştırma

Aşağıdaki komutu çalıştırın:

```bash
!python photo_to_3d_hunyuan.py
```

Alternatif API desteği şu anda sınırlıdır. Bu nedenle script sizden seçim istediğinde çoğu zaman **varsayılan (Default)** değerleri kullanabilirsiniz.

---

# 🎨 Texture Oluşturma (İsteğe Bağlı)

Varsayılan olarak proje yalnızca **3D mesh** üretir.

Texture'lı modeller oluşturmak istiyorsanız Colab ortamınıza ayrıca **Hunyuan3D Paint** modelini kurmanız gerekir.

Script istediğinde model yolunu girmeniz yeterlidir.

---

# 📂 Çıktılar

```text
output/
├── project_1/
├── project_2/
└── ...
```

Her proje kendi oluşturulan 3D modeline sahip olacaktır.

---

# 📌 Notlar

- Yerel (Local) kullanım henüz desteklenmemektedir.
- Gelecek güncellemelerde yerel yapay zeka modelleri ve API desteği eklenmesi planlanmaktadır.

---

# 🤖 Uyumlu Shape Modelleri (Google Colab)

Aşağıdaki **Hunyuan3D Shape modelleri**, bu script ile **Google Colab** ortamında test edilmiş ve uyumlu çalışmaktadır.

| Repository | Alt Klasör | Boyut | Açıklama |
|------------|------------|-------|----------|
| `tencent/Hunyuan3D-2mini` | `hunyuan3d-dit-v2-mini` | 0.6B | Standart Mini model. Hızlı ve hafiftir. |
| `tencent/Hunyuan3D-2mini` | `hunyuan3d-dit-v2-mini-turbo` | 0.6B | **Önerilen model.** En hızlı üretim yapan Mini sürümüdür. |
| `tencent/Hunyuan3D-2mini` | `hunyuan3d-dit-v2-mini-fast` | 0.6B | Hız odaklı alternatif distillation sürümü. |
| `tencent/Hunyuan3D-2` | `hunyuan3d-dit-v2-0` | 1.1B | Daha kaliteli ana model. Daha yavaş ancak daha iyi sonuçlar üretir. |
| `tencent/Hunyuan3D-2` | `hunyuan3d-dit-v2-0-turbo` | 1.1B | Ana modelin hızlandırılmış sürümü. |
| `tencent/Hunyuan3D-2` | `hunyuan3d-dit-v2-0-fast` | 1.1B | Ana modelin alternatif hızlı sürümü. |
| `tencent/Hunyuan3D-2mv` | `hunyuan3d-dit-v2-mv`, `-turbo`, `-fast` | 1.1B | Birden fazla giriş görselini destekleyen Multi-View modelleridir. |
| `tencent/Hunyuan3D-2.1` | `hunyuan3d-dit-v2-1` | 3.0B | En yeni ve en büyük nesildir (Haziran 2025). Daha yüksek VRAM gerektirebilir. |

> 💡 **Öneri:**  
> Google Colab **T4 GPU** için en iyi hız/kalite dengesi **`hunyuan3d-dit-v2-mini-turbo`** modelidir.
>
> > 💙 **Dostane Tavsiye:**  
> Eğer **ücretsiz Google Colab** kullanıyorsanız, **Hunyuan3D-2mini** ve özellikle **Hunyuan3D-2mini Turbo** modellerini tercih etmeniz önerilir. Ücretsiz Colab'ın sunduğu GPU kaynakları için hız ve kalite açısından en dengeli seçeneklerdir.

# ⭐ Katkı

**Seku** tarafından yapay zeka desteğiyle geliştirilmiştir.

❤️ Biraz kahve, biraz yapay zeka.
