import mat73
import scipy.io
import numpy as np
import pandas as pd
import os
from tkinter import filedialog, Tk


def load_mat(file_path):
    try:
        return mat73.loadmat(file_path)
    except Exception:
        raw = scipy.io.loadmat(file_path, squeeze_me=True, struct_as_record=False)
        return {k: v for k, v in raw.items() if not k.startswith('__')}


def struct_to_dict(obj):
    if hasattr(obj, '_fieldnames'):
        return {f: struct_to_dict(getattr(obj, f)) for f in obj._fieldnames}
    if isinstance(obj, np.ndarray) and obj.dtype.names:
        return {n: struct_to_dict(obj[n]) for n in obj.dtype.names}
    return obj


root = Tk()
root.withdraw()
files = filedialog.askopenfilenames(
    title="Select .mat files",
    filetypes=[("MAT files", "*.mat")]
)

if not files:
    print("No files selected.")
else:
    for file_path in files:
        print(f"\nProcessing: {file_path}")

        data = load_mat(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        save_folder = os.path.dirname(file_path)

        print("Loaded keys:", list(data.keys()))

        def save(field_name, content):
            try:
                if hasattr(content, '_fieldnames'):
                    content = struct_to_dict(content)
                df = pd.DataFrame(content)
                csv_path = os.path.join(save_folder, f"{file_name}_{field_name}.csv")
                df.to_csv(csv_path, index=False)
                print(f"  ✓ {field_name} saved -> {csv_path}")
            except Exception as e:
                print(f"  ✗ {field_name} could not be converted: {e}")

        for field_name, content in data.items():
            if field_name.startswith('__'):
                continue
            converted = struct_to_dict(content) if hasattr(content, '_fieldnames') else content
            if isinstance(converted, dict):
                sub_dicts = {k: v for k, v in converted.items() if isinstance(struct_to_dict(v) if hasattr(v, '_fieldnames') else v, dict)}
                if sub_dicts:
                    for sub_name, sub_content in sub_dicts.items():
                        save(f"{field_name}_{sub_name}", sub_content)
                else:
                    save(field_name, converted)
            else:
                save(field_name, converted)

print("\nDone!")
