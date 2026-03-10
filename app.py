from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

from config import Config
from models import db, DonVi, NguoiDung

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return NguoiDung.query.get(int(user_id))

@app.route('/')
def index():
    parent_units = DonVi.query.filter_by(IsParent=True).all()
    return render_template('index.html', parent_units=parent_units)

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    results = []

    if q:
        keyword = f"%{q}%"
        results = DonVi.query.filter(
            or_(
                DonVi.TenDonVi.ilike(keyword),
                DonVi.DiaDiem.ilike(keyword),
                DonVi.Website.ilike(keyword),
                DonVi.Email.ilike(keyword),
                DonVi.DienThoai.ilike(keyword),
                DonVi.MoTa.ilike(keyword)
            )
        ).all()

    return render_template('search.html', q=q, results=results)

@app.route('/parent/<int:id>')
def parent_detail(id):
    parent = DonVi.query.get_or_404(id)
    children = DonVi.query.filter_by(ParentID=id).all()
    return render_template('parent_detail.html', parent=parent, children=children)

@app.route('/unit/<int:id>')
def unit_detail(id):
    unit = DonVi.query.get_or_404(id)
    return render_template('unit_detail.html', unit=unit)

@app.route('/go/<int:id>')
def go_website(id):
    unit = DonVi.query.get_or_404(id)
    if unit.Website:
        website = unit.Website.strip()
        if not website.startswith('http://') and not website.startswith('https://'):
            website = 'https://' + website
        return redirect(website)
    flash('Đơn vị chưa có website')
    return redirect(url_for('unit_detail', id=id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = NguoiDung.query.filter_by(Username=username).first()
        if user and check_password_hash(user.PasswordHash, password):
            login_user(user)
            return redirect(url_for('admin_units'))
        flash('Sai tài khoản hoặc mật khẩu')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/units')
@login_required
def admin_units():
    units = DonVi.query.all()
    return render_template('admin_list.html', units=units)

@app.route('/admin/units/create', methods=['GET', 'POST'])
@login_required
def create_unit():
    parent_units = DonVi.query.filter_by(IsParent=True).all()

    if request.method == 'POST':
        is_parent = request.form.get('is_parent') == 'yes'
        parent_id = request.form.get('parent_id')

        unit = DonVi(
            TenDonVi=request.form.get('ten_don_vi'),
            DiaDiem=request.form.get('dia_diem'),
            Website=request.form.get('website'),
            Email=request.form.get('email'),
            DienThoai=request.form.get('dien_thoai'),
            MoTa=request.form.get('mo_ta'),
            IsParent=is_parent,
            ParentID=None if is_parent else (int(parent_id) if parent_id else None)
        )

        db.session.add(unit)
        db.session.commit()
        return redirect(url_for('admin_units'))

    return render_template('admin_form.html', parent_units=parent_units, unit=None)

@app.route('/admin/units/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_unit(id):
    unit = DonVi.query.get_or_404(id)
    parent_units = DonVi.query.filter_by(IsParent=True).all()

    if request.method == 'POST':
        is_parent = request.form.get('is_parent') == 'yes'

        unit.TenDonVi = request.form.get('ten_don_vi')
        unit.DiaDiem = request.form.get('dia_diem')
        unit.Website = request.form.get('website')
        unit.Email = request.form.get('email')
        unit.DienThoai = request.form.get('dien_thoai')
        unit.MoTa = request.form.get('mo_ta')
        unit.IsParent = is_parent
        unit.ParentID = None if is_parent else int(request.form.get('parent_id'))

        db.session.commit()
        return redirect(url_for('admin_units'))

    return render_template('admin_form.html', parent_units=parent_units, unit=unit)

@app.route('/admin/units/delete/<int:id>', methods=['POST'])
@login_required
def delete_unit(id):
    unit = DonVi.query.get_or_404(id)

    if unit.children:
        flash('Không thể xóa đơn vị cấp 1 khi còn đơn vị cấp 2')
        return redirect(url_for('admin_units'))

    db.session.delete(unit)
    db.session.commit()
    return redirect(url_for('admin_units'))
@app.context_processor
def inject_parent_units():
    parent_units = DonVi.query.filter_by(IsParent=True).order_by(DonVi.TenDonVi.asc()).all()
    return dict(menu_parent_units=parent_units)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if not NguoiDung.query.filter_by(Username='admin').first():
            admin = NguoiDung(
                Username='admin',
                PasswordHash=generate_password_hash('123456'),
                Role='admin'
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)