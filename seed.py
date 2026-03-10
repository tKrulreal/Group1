from app import app
from models import db, DonVi

with app.app_context():
    db.drop_all()
    db.create_all()

    truong_cong_nghe = DonVi(
        TenDonVi="Trường Công nghệ",
        DiaDiem="NEU",
        Website="neu.edu.vn",
        Email="congnghe@neu.edu.vn",
        DienThoai="024xxxxxxx",
        MoTa="Đơn vị cấp 1 quản lý các khoa công nghệ.",
        IsParent=True
    )

    truong_kinh_doanh = DonVi(
        TenDonVi="Trường Kinh doanh",
        DiaDiem="NEU",
        Website="neu.edu.vn",
        Email="kinhdoanh@neu.edu.vn",
        DienThoai="024xxxxxxx",
        MoTa="Đơn vị cấp 1 về lĩnh vực kinh doanh.",
        IsParent=True
    )

    db.session.add_all([truong_cong_nghe, truong_kinh_doanh])
    db.session.commit()

    khoa_cntt = DonVi(
        TenDonVi="Khoa Công nghệ thông tin",
        DiaDiem="Tòa nhà A1",
        Website="fit.neu.edu.vn",
        Email="fit@neu.edu.vn",
        DienThoai="0241111111",
        MoTa="Đơn vị đào tạo CNTT.",
        IsParent=False,
        ParentID=truong_cong_nghe.IDDonVi
    )

    khoa_htttql = DonVi(
        TenDonVi="Khoa Hệ thống thông tin quản lý",
        DiaDiem="Tòa nhà A1",
        Website="mis.neu.edu.vn",
        Email="mis@neu.edu.vn",
        DienThoai="0242222222",
        MoTa="Đơn vị đào tạo MIS.",
        IsParent=False,
        ParentID=truong_cong_nghe.IDDonVi
    )

    khoa_marketing = DonVi(
        TenDonVi="Khoa Marketing",
        DiaDiem="Tòa nhà A2",
        Website="khoamarketing.neu.edu.vn",
        Email="marketing@neu.edu.vn",
        DienThoai="0243333333",
        MoTa="Đơn vị đào tạo marketing.",
        IsParent=False,
        ParentID=truong_kinh_doanh.IDDonVi
    )

    db.session.add_all([khoa_cntt, khoa_htttql, khoa_marketing])
    db.session.commit()

    print("Đã seed dữ liệu mẫu.")