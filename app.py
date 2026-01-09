from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

def init_db():
    """Veritabanı tablosunu bütünleme (-1) varsayılanıyla oluşturur."""
    with sqlite3.connect('btu_obs.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_no TEXT,
                student_name TEXT,
                course_name TEXT,
                vize INTEGER DEFAULT 0,
                final INTEGER DEFAULT 0,
                but INTEGER DEFAULT -1,
                hbp INTEGER DEFAULT 0,
                harf_notu TEXT DEFAULT 'FF'
            )''')
        conn.commit()

def harf_belirle(students, method):
    """Yönerge Tablo 2 ve 3'e göre harf notlarını atar."""
    if not students: return
    
    # Madde 7(5): BDKL (20 puan) sınırı [cite: 43, 46]
    gecerli_hbpler = [s['hbp'] for s in students if s['hbp'] >= 20]
    
    if method == "MNS" or len(students) < 20: # Madde 7(1) ve 9(4) [cite: 41, 74]
        for s in students:
            hbp, exam_notu = s['hbp'], s['exam_notu']
            # Madde 7(3-4): HBP veya sınav notu 35 altıysa FF [cite: 44, 45]
            if exam_notu < 35 or hbp < 35: harf = "FF" 
            elif hbp >= 90: harf = "AA"
            elif hbp >= 80: harf = "BA"
            elif hbp >= 75: harf = "BB"
            elif hbp >= 70: harf = "CB"
            elif hbp >= 65: harf = "CC"
            elif hbp >= 60: harf = "DC"
            elif hbp >= 55: harf = "DD"
            elif hbp >= 35: harf = "FD"
            else: harf = "FF"
            s['harf'] = harf
    else:
        # Bağıl Değerlendirme Sistemi (BDS) [cite: 48, 56]
        ort = np.mean(gecerli_hbpler) if gecerli_hbpler else 0
        std = np.std(gecerli_hbpler) if len(gecerli_hbpler) > 1 else 1
        
        # Tablo 3: T-Skoru Sınıf Düzeyi Limitleri [cite: 54]
        if ort > 80:     limits = [32, 37, 42, 47, 52, 57, 62, 67]
        elif ort > 70:   limits = [34, 39, 44, 49, 54, 59, 64, 69]
        elif ort > 62.5: limits = [36, 41, 46, 51, 56, 61, 66, 71]
        elif ort > 57.5: limits = [38, 43, 48, 53, 58, 63, 68, 73]
        elif ort > 52.5: limits = [40, 45, 50, 55, 60, 65, 70, 75]
        elif ort > 47.5: limits = [42, 47, 52, 57, 62, 67, 72, 77]
        elif ort > 42.5: limits = [44, 49, 54, 59, 64, 69, 74, 79]
        else:            limits = [46, 51, 56, 61, 66, 71, 76, 81]

        for s in students:
            if s['exam_notu'] < 35 or s['hbp'] < 35: s['harf'] = "FF"
            else:
                # T-Skoru Hesaplama [cite: 55]
                t = ((s['hbp'] - ort) / std) * 10 + 60
                harf = "AA"
                harfler = ["FF", "FD", "DD", "DC", "CC", "CB", "BB", "BA", "AA"]
                for i, lim in enumerate(limits):
                    if t < lim:
                        harf = harfler[i]
                        break
                s['harf'] = harf

def hesapla_ve_guncelle(course_name):
    """Sınıf bazlı izolasyon ve büt ayrımı ile hesaplama yapar."""
    with sqlite3.connect('btu_obs.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, vize, final, but FROM Grades WHERE course_name = ?", (course_name,))
        rows = cursor.fetchall()
        
        final_grubu, but_grubu = [], []

        for sid, vize, final, but in rows:
            # Madde 9(4): Büte girenlerin finali sayılmaz 
            exam_notu = but if but != -1 else final
            # Madde 5(2): Vize %40, Final/Büt %60 [cite: 27, 29]
            raw_hbp = (vize * 0.4) + (exam_notu * 0.6)
            # Madde 5(3): 0.50 Yuvarlama kuralı [cite: 28]
            hbp = int(raw_hbp + 0.5) if raw_hbp % 1 >= 0.5 else int(raw_hbp)
            
            s_data = {'id': sid, 'hbp': hbp, 'exam_notu': exam_notu}
            if but != -1: but_grubu.append(s_data)
            else: final_grubu.append(s_data)
            cursor.execute("UPDATE Grades SET hbp = ? WHERE id = ?", (hbp, sid))

        # Final ve Büt grupları ayrı ayrı değerlendirilir [cite: 74]
        harf_belirle(final_grubu, "BDS" if len(final_grubu) >= 20 else "MNS")
        harf_belirle(but_grubu, "BDS" if len(but_grubu) >= 20 else "MNS")

        for s in final_grubu + but_grubu:
            cursor.execute("UPDATE Grades SET harf_notu = ? WHERE id = ?", (s['harf'], s['id']))
        conn.commit()

@app.route('/upload-excel', methods=['POST'])
def upload_excel():
    if 'file' not in request.files: return jsonify({"error": "Dosya yok"}), 400
    file = request.files['file']
    course_name = request.form.get('course_name')
    
    try:
        df = pd.read_excel(file)
        # Sütun isimlerini temizle
        df.columns = [c.strip().lower() for c in df.columns]
        
        with sqlite3.connect('btu_obs.db') as conn:
            cursor = conn.cursor()
            # Sınıf bazlı temizlik
            cursor.execute("DELETE FROM Grades WHERE course_name = ?", (course_name,))
            for _, row in df.iterrows():
                # Excel verilerini çek (Büt boşsa -1 atar)
                b_val = row.get('büt', -1)
                if pd.isna(b_val) or b_val == "": b_val = -1
                
                cursor.execute("""
                    INSERT INTO Grades (student_no, student_name, course_name, vize, final, but) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (str(row.get('öğrenci no', '')), str(row.get('ad soyad', '')), 
                     course_name, int(row.get('vize', 0)), int(row.get('final', 0)), int(b_val)))
            conn.commit()
            hesapla_ve_guncelle(course_name)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-course-grades/<course>', methods=['GET'])
def get_course_grades(course):
    with sqlite3.connect('btu_obs.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Grades WHERE course_name = ?", (course,))
        return jsonify([dict(row) for row in cursor.fetchall()])

@app.route('/update-grade', methods=['POST'])
def update_grade():
    data = request.json
    try:
        sid, v, f, b = int(data['id']), int(data['vize']), int(data['final']), int(data['but'])
        with sqlite3.connect('btu_obs.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT course_name FROM Grades WHERE id = ?", (sid,))
            row = cursor.fetchone()
            if row:
                cursor.execute("UPDATE Grades SET vize = ?, final = ?, but = ? WHERE id = ?", (v, f, b, sid))
                conn.commit()
                hesapla_ve_guncelle(row[0])
                return jsonify({"status": "success"})
    except: return jsonify({"status": "error"}), 400
    return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)