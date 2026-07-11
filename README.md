# 🖼️➡️🧊 pic-to-3d-models
## Convert Any Image into a 3D Model with AI

![AI](https://img.shields.io/badge/AI-Powered-blue)
![Google Colab](https://img.shields.io/badge/Google%20Colab-Compatible-orange)
![License](https://img.shields.io/badge/Usage-User%20Responsible-red)

---

## 🚀 About The Project

This project converts images into 3D models using Artificial Intelligence.

I originally created this tool for my own purposes, but decided to share it with others who might find it useful.

⚠️ **Important:** All legal responsibility regarding the generated content and usage belongs to the user.

The code was developed with the assistance of AI and myself.  
There may still be partial bugs or unexpected behaviors.

💥 **Fully compatible with Google Colab!**

---

# 🇬🇧 English Guide

## 📦 Requirements

Before running the script:

1. Download the AI model locally  
   **or**
2. Save the model to your Google Drive using Hugging Face.

---

## ⚙️ Installation & Usage

### 1️⃣ Prepare Your Model

First, download your desired AI model and copy its path.

Then run the script and enter the model path when requested.

---

### 2️⃣ Input / Output System

After starting the script:

📁 Project Folder ├── script.py ├── input/ └── output/

The script will automatically create:

- 📂 `input` folder
- 📂 `output` folder

---

### 3️⃣ Adding Images

Inside the `input` folder:

1. Create a new folder for your project.
2. Add your reference image(s) inside it.

Example:

input/ └── my_character/ └── image.png

The script will check if images exist and wait until you provide them.

---

## 🧩 Project Structure

Each folder inside `input` represents one 3D generation project.

Example:

input/ ├── car/ │    └── car.png │ └── character/ └── person.jpg

Generated results will be saved with the same folder name inside:

output/ ├── car/ └── character/

---

## 🔄 Automatic Processing System

After a project is processed:

input/ └── character/

will become:

input/ └── character_old/

Folders ending with `_old` are ignored during the next run.

This prevents already processed projects from being generated again.

---

<br>

# 🇹🇷 Türkçe Kullanım

## 📦 Proje Hakkında

Bu proje, yapay zeka kullanarak herhangi bir görseli 3D modele dönüştürür.

Kendi ihtiyaçlarım için geliştirdim, daha sonra başkalarının da kullanabilmesi için paylaşmaya karar verdim.

⚠️ **Önemli:** Oluşturulan içeriklerin kullanımı ve yasal sorumluluğu tamamen kullanıcıya aittir.

Kod, yapay zeka desteği ve benim tarafımdan geliştirilmiştir.  
Kısmi hatalar veya beklenmeyen durumlar olabilir.

💥 **Google Colab ile tamamen uyumludur!**

---

# ⚙️ Kurulum ve Kullanım

## 1️⃣ Model Hazırlama

Öncelikle kullanacağınız modeli:

- Yerel olarak indirin  
veya
- Hugging Face üzerinden Google Drive'a kaydedin.

Daha sonra script çalıştırıldığında model yolunu girin.

---

## 2️⃣ Input / Output Sistemi

Script ilk çalıştırıldığında otomatik olarak:

📁 Proje Dizini ├── script.py ├── input/ └── output/

klasörlerini oluşturur.

---

## 3️⃣ Görsel Ekleme

`input` klasörünün içine yeni bir klasör oluşturun.

Oluşturduğunuz klasörün içine referans görselinizi koyun.

Örnek:

input/ └── karakter/ └── resim.png

Script görsel olup olmadığını kontrol eder ve hazır şekilde bekler.

---

## 🧩 Proje Mantığı

Her `input` klasörü içerisindeki klasör, ayrı bir 3D model üretim işlemidir.

Örnek:

input/ ├── araba/ │    └── araba.png │ └── insan/ └── insan.jpg

Sonuçlar aynı isimle `output` klasörüne kaydedilir:

output/ ├── araba/ └── insan/

---

## 🔄 Otomatik İşlem Takibi

İşlenen klasörlerin sonuna:

_old

eklenir.

Örnek:

Önce:

input/ └── karakter/

Sonra:

input/ └── karakter_old/

şeklinde değişir.

`_old` uzantılı klasörler sonraki çalıştırmalarda tekrar işleme alınmaz.

---

# ⭐ Credits

Developed by: **Seku + AI Assistance**

Made with ❤️ and a little bit of artificial intelligence magic.
