"""
โปรแกรมคำนวณค่าคาดคะเน (Predicted Value) ของสมรรถภาพปอด
สำหรับคนไทย (VC, FEV1, FVC, PEF)
อ้างอิง: Dejsomritrutai W, Nana A, Maranetra N, et al.
Reference spirometric values for healthy lifetime nonsmokers in Thailand.
J Med Assoc Thai 2000; 83: 457-466.

สูตร:
  ชาย:
    VC (ลิตร)  = -2.601 + 0.122A - 0.00046A^2 + 0.00023H^2 - 0.00061AH
    FEV1(ลิตร) = -7.697 + 0.123A + 0.067H - 0.00034A^2 - 0.0007AH
    FVC (ลิตร) = -2.601 + 0.122A - 0.00046A^2 + 0.00023H^2 - 0.00061AH
    PEF (ล./วินาที) = -16.859 + 0.307A + 0.141H - 0.0018A^2 - 0.001AH

  หญิง:
    VC (ลิตร)  = -5.914 + 0.088A + 0.056H - 0.0003A^2 - 0.0005AH
    FEV1(ลิตร) = -10.6 + 0.085A + 0.12H - 0.00019A^2 - 0.00022H^2 - 0.00056AH
    FVC (ลิตร) = -5.914 + 0.088A + 0.056H - 0.0003A^2 - 0.0005AH
    PEF (ล./วินาที) = -31.355 + 0.162A + 0.391H - 0.00084A^2 - 0.00099H^2 - 0.00072AH

  H = ความสูง (เซนติเมตร), A = อายุ (ปี)
"""


def calc_predicted(gender, age, height):
    A = age
    H = height

    if gender == "male":
        vc = -2.601 + 0.122 * A - 0.00046 * A**2 + 0.00023 * H**2 - 0.00061 * A * H
        fev1 = -7.697 + 0.123 * A + 0.067 * H - 0.00034 * A**2 - 0.0007 * A * H
        fvc = -2.601 + 0.122 * A - 0.00046 * A**2 + 0.00023 * H**2 - 0.00061 * A * H
        pef = -16.859 + 0.307 * A + 0.141 * H - 0.0018 * A**2 - 0.001 * A * H
    else:  # female
        vc = -5.914 + 0.088 * A + 0.056 * H - 0.0003 * A**2 - 0.0005 * A * H
        fev1 = -10.6 + 0.085 * A + 0.12 * H - 0.00019 * A**2 - 0.00022 * H**2 - 0.00056 * A * H
        fvc = -5.914 + 0.088 * A + 0.056 * H - 0.0003 * A**2 - 0.0005 * A * H
        pef = -31.355 + 0.162 * A + 0.391 * H - 0.00084 * A**2 - 0.00099 * H**2 - 0.00072 * A * H

    return {"VC": vc, "FEV1": fev1, "FVC": fvc, "PEF": pef}


def percent_predicted(measured, predicted):
    if predicted == 0:
        return 0.0
    return measured / predicted * 100


def get_float(prompt_text):
    while True:
        try:
            return float(input(prompt_text).strip())
        except ValueError:
            print("กรุณากรอกตัวเลขให้ถูกต้อง")


def get_gender():
    while True:
        g = input("เพศ (ช/ญ หรือ M/F): ").strip().lower()
        if g in ("ช", "m", "male", "ชาย"):
            return "male"
        if g in ("ญ", "f", "female", "หญิง"):
            return "female"
        print("กรุณากรอก ช หรือ ญ (หรือ M/F)")


def main():
    print("=== โปรแกรมคำนวณค่าคาดคะเนสมรรถภาพปอด (Spirometry Predicted Value) ===\n")

    gender = get_gender()
    age = get_float("อายุ (ปี): ")
    height = get_float("ความสูง (เซนติเมตร): ")

    predicted = calc_predicted(gender, age, height)

    print("\n--- ค่าคาดคะเน (Predicted Value) ---")
    print(f"VC   = {predicted['VC']:.3f} ลิตร")
    print(f"FEV1 = {predicted['FEV1']:.3f} ลิตร")
    print(f"FVC  = {predicted['FVC']:.3f} ลิตร")
    print(f"PEF  = {predicted['PEF']:.3f} ลิตร/วินาที")

    ans = input("\nต้องการกรอกค่าที่วัดได้จริงเพื่อคำนวณ % ของค่าคาดคะเนหรือไม่? (y/n): ").strip().lower()
    if ans == "y":
        print("\nกรอกค่าที่วัดได้จริง:")
        measured_vc = get_float("VC ที่วัดได้ (ลิตร): ")
        measured_fev1 = get_float("FEV1 ที่วัดได้ (ลิตร): ")
        measured_fvc = get_float("FVC ที่วัดได้ (ลิตร): ")
        measured_pef = get_float("PEF ที่วัดได้ (ลิตร/วินาที): ")

        print("\n--- ผลลัพธ์ ---")
        print(f"{'ค่า':<8}{'วัดได้':>10}{'คาดคะเน':>12}{'% คาดคะเน':>14}")
        rows = [
            ("VC", measured_vc, predicted["VC"]),
            ("FEV1", measured_fev1, predicted["FEV1"]),
            ("FVC", measured_fvc, predicted["FVC"]),
            ("PEF", measured_pef, predicted["PEF"]),
        ]
        for name, measured, pred in rows:
            pct = percent_predicted(measured, pred)
            print(f"{name:<8}{measured:>10.3f}{pred:>12.3f}{pct:>13.1f}%")

    print("\nเสร็จสิ้น")


if __name__ == "__main__":
    main()
