from typing import Dict, List, Optional
import requests
from google.adk.agents import Agent

# Session HTTP global untuk efisiensi koneksi API
SESSION = requests.Session()
BASE_URL = "https://www.themealdb.com/api/json/v1/1"

def cari_resep_makanan(kata_kunci: str) -> Dict[str, object]:
    """
    Mencari resep masakan berdasarkan nama hidangan atau bahan utama (seperti ayam, telur, sapi, dll)
    menggunakan REST API TheMealDB.

    Args:
        kata_kunci: Nama makanan atau bahan utama (disarankan dalam bahasa Inggris, misal: 'chicken', 'egg', 'beef', 'pasta').

    Returns:
        Dict berisi status dan daftar resep yang ditemukan beserta bahan dan langkah memasaknya.
    """
    try:
        print(f"[INFO] Memanggil API TheMealDB untuk kata kunci: '{kata_kunci}'")
        
        # 1. Cari berdasarkan nama resep
        response = SESSION.get(f"{BASE_URL}/search.php?s={kata_kunci}", timeout=8)
        data = response.json()
        meals = data.get("meals")

        # 2. Jika tidak ada hasil, coba cari berdasarkan bahan utama (filter by ingredient)
        if not meals:
            response_ing = SESSION.get(f"{BASE_URL}/filter.php?i={kata_kunci}", timeout=8)
            data_ing = response_ing.json()
            filtered_meals = data_ing.get("meals")
            
            if filtered_meals:
                meals = []
                # Ambil detail resep lengkap untuk maksimal 3 menu teratas
                for m in filtered_meals[:3]:
                    meal_id = m.get("idMeal")
                    detail_res = SESSION.get(f"{BASE_URL}/lookup.php?i={meal_id}", timeout=8)
                    detail_data = detail_res.json()
                    if detail_data.get("meals"):
                        meals.append(detail_data["meals"][0])

        if not meals:
            return {
                "status": "error",
                "error_message": f"Tidak ditemukan resep untuk kata kunci '{kata_kunci}'."
            }

        resep_list: List[Dict[str, object]] = []
        
        # Ekstrak maksimal 3 resep
        for meal in meals[:3]:
            # Gabungkan nama bahan (strIngredientX) dan takarannya (strMeasureX)
            bahan_list = []
            for i in range(1, 21):
                ing = meal.get(f"strIngredient{i}")
                meas = meal.get(f"strMeasure{i}")
                if ing and ing.strip():
                    takaran = meas.strip() if meas else ""
                    bahan_list.append(f"{ing.strip()} ({takaran})".strip())

            resep_list.append({
                "nama_makanan": meal.get("strMeal"),
                "kategori": meal.get("strCategory"),
                "asal_daerah": meal.get("strArea"),
                "bahan_bahan": bahan_list,
                "cara_memasak": meal.get("strInstructions"),
                "gambar": meal.get("strMealThumb"),
                "video_youtube": meal.get("strYoutube")
            })

        return {"status": "success", "daftar_resep": resep_list}

    except Exception as e:
        return {"status": "error", "error_message": f"Gagal mengambil data resep: {str(e)}"}


# Inisialisasi Agent Rekomendasi Resep & Nutrisi
root_agent = Agent(
    name="resep_nutrisi_agent",
    model="gemini-2.5-flash",
    description="Agent konsultan kuliner dan rekomendasi resep sehat berbasis API TheMealDB.",
    instruction=(
        "Anda adalah seorang Koki Profesional sekaligus Konsultan Nutrisi Sehat.\n\n"
        "Tugas utama Anda:\n"
        "1. Bantu pengguna mencari resep masakan berdasarkan masukan bahan atau nama hidangan.\n"
        "2. Gunakan tool 'cari_resep_makanan'. (Tips: Terjemahkan kata kunci bahan/makanan dari pengguna ke bahasa Inggris saat memanggil tool, contoh: 'ayam' -> 'chicken', 'telur' -> 'egg', 'nasi' -> 'rice').\n"
        "3. Sajikan respon dalam Bahasa Indonesia dengan struktur rapi:\n"
        "   - **Nama & Kategori Hidangan**\n"
        "   - **Bahan-Bahan**: Terjemahkan daftar bahan ke Bahasa Indonesia agar pengguna mudah memahami.\n"
        "   - **Langkah-Langkah Pembuatan**: Tulis langkah memasak secara urut dan jelas.\n"
        "   - **Analisis & Tips Nutrisi**: Tulis estimasi kandungan nutrisi (kalori, protein, karbohidrat, atau lemak) serta saran modifikasi agar resep menjadi lebih sehat (misal: mengurangi minyak, ganti gula dengan madu, dll).\n"
    ),
    tools=[cari_resep_makanan],
)