# 🥗 Agent Rekomendasi Resep & Nutrisi dengan Google ADK

Agent cerdas yang dibangun menggunakan [Google Agent Development Kit (ADK)](https://ai.google.dev/) untuk **mencari resep masakan, menyusun langkah memasak, dan memberikan analisis nutrisi sehat**. Agent ini terintegrasi dengan REST API [TheMealDB](https://www.themealdb.com/) sehingga memberikan respon yang cepat, akurat, dan bebas dari kendala *scraping* atau pemblokiran IP.

---

## 🚀 Fitur Utama

- 🍳 **Pencarian Resep Cerdas:** Mencari resep berdasarkan nama hidangan atau bahan makanan utama (ayam, telur, pasta, dll).
- 🥦 **Analisis & Tips Nutrisi:** Memberikan estimasi gizi serta saran modifikasi agar masakan jadi lebih sehat.
- 🌐 **Multi-Bahasa (Auto Translation):** Menerima kueri Bahasa Indonesia dan menerjemahkan bahan masakan ke Bahasa Indonesia secara rapi.
- ⚡ **100% Bebas Blokir:** Menggunakan REST API murni dalam format JSON, sehingga waktu respons sangat cepat dan stabil.
- ⚙️ **Powered by Gemini:** Menggunakan model `gemini-2.5-flash` melalui Google ADK.

---

## 📦 Prasyarat

Sebelum menjalankan agent ini, pastikan Anda telah menginstal pustaka yang dibutuhkan:

```bash
pip install google-adk requests