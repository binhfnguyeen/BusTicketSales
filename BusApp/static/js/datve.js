window.onload = function() {
    fetch("/api/vitri")
        .then(response => response.json())
        .then(data => {
            const diemDiSelect = document.querySelector('select[name="diem_di"]');
            const diemDenSelect = document.querySelector('select[name="diem_den"]');
            const quanHuyenDiSelect = document.querySelector('select[name="quan_huyen_di"]')
            const benDiSelect = document.querySelector('select[name="ben_di"]')
            const quanHuyenDenSelect = document.querySelector('select[name="quan_huyen_den"]')
            const benDenSelect = document.querySelector('select[name="ben_den"]')
            data.diem_di.forEach(diem => {
                diemDiSelect.innerHTML += `<option value="${diem}">${diem}</option>`;
            });
            data.diem_den.forEach(diem => {
                diemDenSelect.innerHTML += `<option value="${diem}">${diem}</option>`;
            });
            data.quan_huyen_di.forEach(quan=>{
                quanHuyenDiSelect.innerHTML += `<option value="${quan}">${quan}</option>`
            })
            data.quan_huyen_den.forEach(quan=>{
                quanHuyenDenSelect.innerHTML += `<option value="${quan}">${quan}</option>`
            })
            data.ben_di.forEach(ben=>{
                benDiSelect.innerHTML+= `<option value="${ben}">${ben}</option>`
            })
            data.ben_den.forEach(ben=>{
                benDenSelect.innerHTML+= `<option value="${ben}">${ben}</option>`
            })
        })
        .catch(error => console.error('Error fetching data:', error));
};

let diemDi;
let diemDen;
let quanHuyenDi;
let quanHuyenDen;
let benDi;
let benDen;

function getDiemDi(value){
    diemDi = value;
    console.log(diemDi);
}

function getDiemDen(value){
    diemDen = value;
    console.log(diemDen)
}

function getQuanHuyenDi(value){
    quanHuyenDi = value;
    console.log(quanHuyenDi)
}

function getQuanHuyenDen(value){
    quanHuyenDen = value;
    console.log(quanHuyenDen);
}

function getBenDi(value){
    benDi = value;
    console.log(benDi);
}

function getBenDen(value){
    benDen = value;
    console.log(benDen)
}

function cssResult(ngayDi, ngayVe) {
    return `
        <div class="d-flex flex-wrap justify-content-center" id="resultContainer">
            <div class="card mb-3" style="width: 30%;">
                <div class="card-body">
                    <div class="container-sm">
                        <table class="table table-bordered table-striped table-sm">
                            <tbody>
                                <tr><td><strong>Giá vé</strong></td><td><span>150k</span></td></tr>
                                <tr><td><strong>Loại</strong></td><td><span>Giường nằm</span></td></tr>
                                <tr><td><strong>Số chỗ</strong></td><td><span>30</span></td></tr>
                                <tr><td><strong>Ngày đi</strong></td><td><span>${ngayDi}</span></td></tr>
                                <tr><td><strong>Ngày về</strong></td><td><span>${ngayVe}</span></td></tr>
                                <tr><td><strong>Điểm đi</strong></td><td><span>${diemDi}</span></td></tr>
                                <tr><td><strong>Điểm đến</strong></td><td><span>${diemDen}</span></td></tr>
                                <tr><td><strong>Biển số</strong></td><td><span>65D1-50354</span></td></tr>
                                <tr><td><strong>Giá vé</strong></td><td><span>180k</span></td></tr>
                                <tr><td><strong>Tổng số vé</strong></td><td><span>2</span></td></tr>
                                <tr><td><strong>Tổng tiền</strong></td><td><span>360k</span></td></tr>
                            </tbody>
                        </table>
                        <a href="/thanhtoan" class="btn btn-primary btn-sm">Đặt vé</a>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function showResult() {
    document.querySelector('.bresult').style.display = 'none';
    const ngayDi = document.getElementById("ngaydi").value;
    const ngayVe = document.getElementById("ngayve").value;

    if (diemDi && diemDen && ngayDi && ngayVe) {
        const resultHtml = cssResult(ngayDi, ngayVe);
        document.getElementById('resultContainer').outerHTML = resultHtml;
        document.querySelector('.bresult').style.display = 'block';
    } else {
        alert("Vui lòng chọn đủ thông tin!");
    }
}

function showFilterResult(){
    document.querySelector('.bresult').style.display = 'none';
    const ngayDi = document.getElementById("ngaydi").value;
    const ngayVe = document.getElementById("ngayve").value;

        if (diemDi && diemDen && ngayDi && ngayVe && quanHuyenDi && quanHuyenDen && benDi && benDen){
            document.getElementById('resultContainer').outerHTML=`
                <div class="d-flex flex-wrap justify-content-center" id="resultContainer">
                    <div class="card mb-3" style="width: 30%;">
                        <div class="card-body">
                            <div class="container-sm">
                                <table class="table table-bordered table-striped table-sm">
                                    <tbody>
                                        <tr><td><strong>Giá vé</strong></td><td><span>150k</span></td></tr>
                                        <tr><td><strong>Loại</strong></td><td><span>Giường nằm</span></td></tr>
                                        <tr><td><strong>Số chỗ</strong></td><td><span>30</span></td></tr>
                                        <tr><td><strong>Bến đi</strong></td><td><span>${benDi}</span></td></tr>
                                        <tr><td><strong>Bến đến</strong></td><td><span>${benDen}</span></td></tr>
                                        <tr><td><strong>Ngày đi</strong></td><td><span>${ngayDi}</span></td></tr>
                                        <tr><td><strong>Ngày về</strong></td><td><span>${ngayVe}</span></td></tr>
                                        <tr><td><strong>Điểm đi</strong></td><td><span>${diemDi}</span></td></tr>
                                        <tr><td><strong>Điểm đến</strong></td><td><span>${diemDen}</span></td></tr>
                                        <tr><td><strong>Biển số</strong></td><td><span>65D1-50354</span></td></tr>
                                        <tr><td><strong>Giá vé</strong></td><td><span>180k</span></td></tr>
                                        <tr><td><strong>Tổng số vé</strong></td><td><span>2</span></td></tr>
                                        <tr><td><strong>Tổng tiền</strong></td><td><span>360k</span></td></tr>
                                    </tbody>
                                </table>
                                <a href="/thanhtoan" class="btn btn-primary btn-sm">Đặt vé</a>
                            </div>
                        </div>
                    </div>
                </div>`;
                document.querySelector('.bresult').style.display = 'block';
        } else
            alert("Vui lòng chọn đủ thông tin!");
}

