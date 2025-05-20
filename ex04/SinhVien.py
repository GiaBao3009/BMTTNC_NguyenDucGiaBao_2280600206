class SinhVien:
    def __init__(self, id, name, sex, age, diemToan, diemLy, diemHoa):
        self.id = id
        self.name = name
        self.sex = sex
        self.age = age
        self.diemToan = diemToan
        self.diemLy = diemLy
        self.diemHoa = diemHoa
        self.diemTB = 0
        self.hocLuc = ""

    def tinhDiemTB(self):
        self.diemTB = round((self.diemToan + self.diemLy + self.diemHoa) / 3, 2)

    def xepLoaiHocLuc(self):
        if (self.diemTB >= 8):
            self.hocLuc = "Gioi"
        elif (self.diemTB >= 6.5):
            self.hocLuc = "Kha"
        elif (self.diemTB >= 5):
            self.hocLuc = "Trung Binh"
        else:
            self.hocLuc = "Yeu"

    def toString(self):
        return f"ID: {self.id}, Ten: {self.name}, Gioi tinh: {self.sex}, Tuoi: {self.age}, Diem TB: {self.diemTB}, Hoc luc: {self.hocLuc}"
