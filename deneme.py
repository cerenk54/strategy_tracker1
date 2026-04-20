import mat73
import scipy.io
import numpy as np
import pandas as pd
import os
from tkinter import filedialog, Tk


def load_mat(dosya_yolu):
    try:
        return mat73.loadmat(dosya_yolu)
    except Exception:
        raw = scipy.io.loadmat(dosya_yolu, squeeze_me=True, struct_as_record=False)
        return {k: v for k, v in raw.items() if not k.startswith('__')}


def struct_to_dict(obj):
    if hasattr(obj, '_fieldnames'):
        return {f: struct_to_dict(getattr(obj, f)) for f in obj._fieldnames}
    if isinstance(obj, np.ndarray) and obj.dtype.names:
        return {n: struct_to_dict(obj[n]) for n in obj.dtype.names}
    return obj


root = Tk()
root.withdraw()
dosyalar = filedialog.askopenfilenames(
    title="Mat dosyalarını seç",
    filetypes=[("MAT files", "*.mat")]
)

if not dosyalar:
    print("Hiç dosya seçilmedi.")
else:
    for dosya_yolu in dosyalar:
        print(f"\nİşleniyor: {dosya_yolu}")

        veri = load_mat(dosya_yolu)
        dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
        kayit_klasoru = os.path.dirname(dosya_yolu)

        print("Yüklenen anahtarlar:", list(veri.keys()))

        def kaydet(alan_adi, icerik):
            try:
                if hasattr(icerik, '_fieldnames'):
                    icerik = struct_to_dict(icerik)
                df = pd.DataFrame(icerik)
                csv_yolu = os.path.join(kayit_klasoru, f"{dosya_adi}_{alan_adi}.csv")
                df.to_csv(csv_yolu, index=False)
                print(f"  ✓ {alan_adi} kaydedildi -> {csv_yolu}")
            except Exception as e:
                print(f"  ✗ {alan_adi} dönüştürülemedi: {e}")

        for alan_adi, icerik in veri.items():
            if alan_adi.startswith('__'):
                continue
            converted = struct_to_dict(icerik) if hasattr(icerik, '_fieldnames') else icerik
            if isinstance(converted, dict):
                sub_dicts = {k: v for k, v in converted.items() if isinstance(struct_to_dict(v) if hasattr(v, '_fieldnames') else v, dict)}
                if sub_dicts:
                    for sub_adi, sub_icerik in sub_dicts.items():
                        kaydet(f"{alan_adi}_{sub_adi}", sub_icerik)
                else:
                    kaydet(alan_adi, converted)
            else:
                kaydet(alan_adi, converted)

print("\nTamamlandı!")
