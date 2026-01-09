import React, { useState } from 'react';

const BTUPortali = () => {
  const [user, setUser] = useState(null); // { role: 'hoca'|'ogrenci', name: string, studentNo?: string }
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [selectedClass, setSelectedClass] = useState(null);
  const [ogrenciler, setOgrenciler] = useState([]);

  // Backend adresi
  const API_URL = "http://127.0.0.1:5000";

  // --- 1. GİRİŞ SİSTEMİ ---
  const handleLogin = () => {
    // Hoca Giriş Bilgileri
    if (email === "ali.hoca@btu.edu.tr" && password === "Btu55095!") {
      setUser({ role: 'hoca', name: 'Ali Hoca' });
    } 
    // Öğrenci Giriş Bilgileri
    else if (email === "ahmet.ogr@btu.edu.tr" && password === "Btu11225!") {
      setUser({ role: 'ogrenci', name: 'Ahmet Öğrenci', studentNo: '22010101' });
      fetchOgrenciNotu('22010101');
    } 
    else {
      alert("Hatalı e-posta veya şifre!");
    }
  };

  // --- 2. VERİ İŞLEMLERİ (HOCA) ---
  const verileriGetir = async (className) => {
    try {
      const response = await fetch(`${API_URL}/get-course-grades/${className}`);
      const data = await response.json();
      setOgrenciler(data);
      setSelectedClass(className);
    } catch (error) {
      alert("Sunucuya bağlanılamadı!");
    }
  };

  const excelYukle = async (e) => {
    const file = e.target.files[0];
    if (!selectedClass) {
      alert("Lütfen önce bir sınıf seçin!");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('course_name', selectedClass);

    try {
      const response = await fetch(`${API_URL}/upload-excel`, {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        alert("Excel başarıyla yüklendi ve notlar hesaplandı!");
        verileriGetir(selectedClass);
      } else {
        alert("Yükleme hatası!");
      }
    } catch (err) {
      alert("Bağlantı hatası!");
    }
  };

  const notGuncelle = async (id, vize, final, butInput) => {
    // Büt boşsa -1 göndererek finalin sayılmasını sağlarız
    const butValue = (butInput === "" || butInput === null) ? -1 : parseInt(butInput);
    
    await fetch(`${API_URL}/update-grade`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, vize: parseInt(vize), final: parseInt(final), but: butValue })
    });
    verileriGetir(selectedClass);
  };

  // --- 3. VERİ İŞLEMLERİ (ÖĞRENCİ) ---
  const fetchOgrenciNotu = async (no) => {
    try {
      const resA = await fetch(`${API_URL}/get-course-grades/Sinif-A`);
      const resB = await fetch(`${API_URL}/get-course-grades/Sinif-B`);
      const hepsi = [...await resA.json(), ...await resB.json()];
      const ben = hepsi.find(s => s.student_no === no);
      setOgrenciler(ben ? [ben] : []);
    } catch (e) {
      console.error("Notlar çekilemedi");
    }
  };

  // --- ARAYÜZ: GİRİŞ EKRANI ---
  if (!user) {
    return (
      <div className="min-h-screen bg-slate-100 flex items-center justify-center p-6">
        <div className="bg-white p-12 rounded-[3rem] shadow-2xl max-w-sm w-full border-t-8 border-indigo-600">
          <div className="w-20 h-20 bg-indigo-600 rounded-3xl mx-auto mb-8 flex items-center justify-center text-white text-3xl font-black shadow-lg shadow-indigo-200">BTÜ</div>
          <h2 className="text-2xl font-black text-center mb-8 text-slate-800 uppercase tracking-tighter italic">OBS GİRİŞ</h2>
          <div className="space-y-6">
            <input type="email" placeholder="E-posta" className="w-full p-4 bg-slate-50 rounded-2xl border-2 border-transparent focus:border-indigo-500 outline-none font-bold" onChange={(e) => setEmail(e.target.value)} />
            <input type="password" placeholder="Şifre" className="w-full p-4 bg-slate-50 rounded-2xl border-2 border-transparent focus:border-indigo-500 outline-none font-bold" onChange={(e) => setPassword(e.target.value)} />
            <button onClick={handleLogin} className="w-full py-5 bg-indigo-600 text-white rounded-2xl font-black shadow-xl hover:bg-indigo-700 transition-all uppercase tracking-widest">Sisteme Gir</button>
          </div>
        </div>
      </div>
    );
  }

  // --- ARAYÜZ: ANA PANEL ---
  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-12 font-sans">
      <div className="max-w-6xl mx-auto">
        <header className="flex justify-between items-center mb-12">
          <div>
            <h1 className="text-3xl font-black text-slate-900 tracking-tighter uppercase italic">BTÜ NOT SİSTEMİ</h1>
            <p className="text-indigo-600 font-bold text-xs uppercase tracking-widest mt-1">Hoş Geldiniz, {user.name}</p>
          </div>
          <button onClick={() => window.location.reload()} className="px-6 py-2 bg-white text-rose-500 rounded-xl font-black text-xs shadow-sm border border-rose-100 hover:bg-rose-50 transition-all uppercase tracking-widest">Çıkış</button>
        </header>

        {user.role === 'hoca' ? (
          <>
            {/* SINIF SEÇİMİ [cite: 41, 42] */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
              <button onClick={() => verileriGetir('Sinif-A')} className={`p-10 rounded-[2.5rem] text-left transition-all border-4 ${selectedClass === 'Sinif-A' ? 'bg-indigo-600 border-indigo-200 text-white shadow-2xl scale-105' : 'bg-white border-transparent text-slate-600 shadow-md hover:border-indigo-400'}`}>
                <div className="font-black text-2xl uppercase italic">SINIF A</div>
                <div className="text-sm font-bold opacity-70 mt-1">15 Öğrenci (Mutlak - MNS)</div>
              </button>
              <button onClick={() => verileriGetir('Sinif-B')} className={`p-10 rounded-[2.5rem] text-left transition-all border-4 ${selectedClass === 'Sinif-B' ? 'bg-indigo-600 border-indigo-200 text-white shadow-2xl scale-105' : 'bg-white border-transparent text-slate-600 shadow-md hover:border-indigo-400'}`}>
                <div className="font-black text-2xl uppercase italic">SINIF B</div>
                <div className="text-sm font-bold opacity-70 mt-1">25 Öğrenci (Bağıl - BDS)</div>
              </button>
            </div>

            {/* ÖĞRENCİ LİSTESİ */}
            {selectedClass && (
              <div className="bg-white rounded-[3rem] shadow-xl overflow-hidden border border-slate-200">
                <div className="p-8 bg-slate-50 border-b flex justify-between items-center">
                  <h3 className="font-black text-slate-700 tracking-widest uppercase italic">{selectedClass} Öğrenci Listesi</h3>
                  <label className="bg-emerald-600 text-white px-6 py-3 rounded-2xl font-black text-xs cursor-pointer hover:bg-emerald-700 transition-all shadow-lg hover:scale-105 active:scale-95">
                    EXCEL'DEN AKTAR
                    <input type="file" className="hidden" accept=".xlsx,.xls" onChange={excelYukle} />
                  </label>
                </div>
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-slate-50/50 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                      <th className="p-8">Öğrenci No</th>
                      <th className="p-8">Ad Soyad</th>
                      <th className="p-8 text-center">Vize (%40)</th>
                      <th className="p-8 text-center">Final (%60)</th>
                      <th className="p-8 text-center bg-amber-50 text-amber-600 italic">Bütünleme</th>
                      <th className="p-8 text-center">HBP</th>
                      <th className="p-8 text-center">Harf</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 font-bold text-slate-700">
                    {ogrenciler.map(o => (
                      <tr key={o.id} className="hover:bg-slate-50/50 transition-colors">
                        <td className="p-8 text-slate-400 text-sm italic">{o.student_no}</td>
                        <td className="p-8 uppercase">{o.student_name}</td>
                        <td className="p-8 text-center">
                          <input type="number" defaultValue={o.vize} className="w-16 border-2 border-slate-100 rounded-xl p-2 text-center font-black focus:border-indigo-500 outline-none" onBlur={(e) => notGuncelle(o.id, e.target.value, o.final, o.but)} />
                        </td>
                        <td className="p-8 text-center">
                          <input type="number" defaultValue={o.final} className={`w-16 border-2 border-slate-100 rounded-xl p-2 text-center font-black focus:border-indigo-500 outline-none ${o.but !== -1 ? 'opacity-30' : ''}`} disabled={o.but !== -1} onBlur={(e) => notGuncelle(o.id, o.vize, e.target.value, o.but)} />
                        </td>
                        <td className="p-8 text-center bg-amber-50/20">
                          <input type="number" placeholder="-" value={o.but === -1 ? "" : o.but} className="w-16 border-2 border-amber-200 rounded-xl p-2 text-center font-black text-amber-700 outline-none focus:border-amber-500" onChange={(e) => {
                            const val = e.target.value;
                            const newRows = [...ogrenciler];
                            const target = newRows.find(x => x.id === o.id);
                            target.but = val === "" ? -1 : parseInt(val);
                            setOgrenciler(newRows);
                          }} onBlur={(e) => notGuncelle(o.id, o.vize, o.final, e.target.value)} />
                        </td>
                        <td className="p-8 text-center font-black text-indigo-600 text-lg">{o.hbp}</td>
                        <td className="p-8 text-center">
                          <span className={`px-5 py-2 rounded-2xl font-black text-xs ${o.harf_notu === 'FF' ? 'bg-rose-100 text-rose-600' : 'bg-emerald-100 text-emerald-600'}`}>
                            {o.harf_notu}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        ) : (
          /* ÖĞRENCİ PANELİ [cite: 18] */
          <div className="bg-indigo-950 text-white p-16 rounded-[4rem] text-center max-w-md mx-auto shadow-2xl border border-white/10 mt-10">
            <h2 className="text-9xl font-black mb-4 text-emerald-400 drop-shadow-2xl">{ogrenciler[0]?.harf_notu}</h2>
            <p className="opacity-40 uppercase text-[10px] font-black tracking-[0.3em] mb-12">Harf Notunuz</p>
            <div className="grid grid-cols-2 gap-4 border-t border-white/5 pt-10">
              <div className="bg-white/5 p-6 rounded-3xl border border-white/5">
                <div className="text-[10px] opacity-30 uppercase font-black mb-2">Başarı Puanı</div>
                <div className="text-2xl font-black">{ogrenciler[0]?.hbp}</div>
              </div>
              {ogrenciler[0]?.but !== -1 && (
                <div className="bg-amber-500/10 p-6 rounded-3xl border border-amber-500/10">
                  <div className="text-[10px] text-amber-400 uppercase font-black mb-2">Bütünleme</div>
                  <div className="text-2xl font-black text-amber-400">{ogrenciler[0]?.but}</div>
                </div>
              )}
            </div>
            <p className="mt-10 text-[9px] text-white/20 italic">BTÜ Ölçme ve Değerlendirme Esasları Madde 5, 7 ve 9 uyarınca hesaplanmıştır.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BTUPortali;