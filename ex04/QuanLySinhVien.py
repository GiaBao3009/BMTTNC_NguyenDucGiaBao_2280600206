from SinhVien import SinhVien

class QuanLySinhVien:
    listSinhVien = []

    def generateID(self):
        maxid = 0
        if (self.soluongSinhVien() > 0):
            maxid = self.listSinhVien[0].id
            for sv in self.listSinhVien:
                if (maxid < sv.id):
                    maxid = sv.id
        maxid = maxid + 1
        return maxid

    def soluongSinhVien(self):
        return self.listSinhVien.__len__()

    def nhapSinhVien(self):
        svid = self.generateID()
        name = input("Nhap ten sinh vien: ")
        sex = input("Nhap gioi tinh sinh vien: ")
        age = int(input("Nhap tuoi sinh vien: "))
        diemToan = float(input("Nhap diem Toan: "))
        diemLy = float(input("Nhap diem Ly: "))
        diemHoa = float(input("Nhap diem Hoa: "))
        sv = SinhVien(svid, name, sex, age, diemToan, diemLy, diemHoa)
        sv.tinhDiemTB()
        sv.xepLoaiHocLuc()
        self.listSinhVien.append(sv)

    def updateSinhVien(self, ID):
        sv: SinhVien = self.findByID(ID)
        if (sv != None):
            name = input("Nhap ten sinh vien: ")
            sex = input("Nhap gioi tinh sinh vien: ")
            age = int(input("Nhap tuoi sinh vien: "))
            diemToan = float(input("Nhap diem Toan: "))
            diemLy = float(input("Nhap diem Ly: "))
            diemHoa = float(input("Nhap diem Hoa: "))
            sv.name = name
            sv.sex = sex
            sv.age = age
            sv.diemToan = diemToan
            sv.diemLy = diemLy
            sv.diemHoa = diemHoa
            sv.tinhDiemTB()
            sv.xepLoaiHocLuc()
        else:
            print("Sinh vien co ID = {} khong ton tai.".format(ID))

    def sortByID(self):
        self.listSinhVien.sort(key=lambda x: x.id, reverse=False)

    def sortByName(self):
        self.listSinhVien.sort(key=lambda x: x.name, reverse=False)

    def sortByDiemTB(self):
        self.listSinhVien.sort(key=lambda x: x.diemTB, reverse=False)

    def findByID(self, ID):
        searchResult = None
        if (self.soluongSinhVien() > 0):
            for sv in self.listSinhVien:
                if (sv.id == ID):
                    searchResult = sv
                    return searchResult
        return searchResult

    def findByName(self, keyword):
        listSV = []
        if (self.soluongSinhVien() > 0):
            for sv in self.listSinhVien:
                if (keyword.upper() in sv.name.upper()):
                    listSV.append(sv)
        return listSV

    def deleteById(self, ID):
        isDeleted = False
        sv = self.findByID(ID)
        if (sv != None):
            self.listSinhVien.remove(sv)
            isDeleted = True
        return isDeleted

    def showSinhVien(self, listSV):
        print("{:<8} {:<18} {:<8} {:<8} {:<8} {:<8}".format("ID", "Name", "Sex", "Age", "Diem TB", "Hoc Luc"))
        if (listSV.__len__() > 0):
            for sv in listSV:
                print("{:<8} {:<18} {:<8} {:<8} {:<8} {:<8}".format(sv.id, sv.name, sv.sex, sv.age, sv.diemTB, sv.hocLuc))
        print("\n")

    def getListSinhVien(self):
        return self.listSinhVien