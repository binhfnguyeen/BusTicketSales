function showResult() {
    var diemDi = document.querySelector('[name="diem_di"]').value;
    var diemDen = document.querySelector('[name="diem_den"]').value;
    var benDi = document.querySelector('[name="ben_di"]').value;
    var benDen = document.querySelector('[name="ben_den"]').value;
    var ngayDi = document.getElementById('ngaydi').value;
    var ngayVe = document.getElementById('ngayve').value;
    var choNgoi = document.querySelector('[name="chongoi"]').value;
    localStorage.setItem('ngayDi', ngayDi);
    localStorage.setItem('ngayVe', ngayVe);
    localStorage.setItem('choNgoi', choNgoi);

    fetch(`/api/chuyenxe?diem_di=${diemDi}&diem_den=${diemDen}&ben_di=${benDi}&ben_den=${benDen}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === "found") {
                console.log("Tìm thấy chuyến xe:", data.data);
                var resultContainer = document.getElementById('resultContainer');
                resultContainer.innerHTML = '';
                data.data.forEach(chuyenxe => {
                    localStorage.setItem('diemDi', diemDi);
                    localStorage.setItem('diemDen', diemDen);
                    localStorage.setItem('benDi', benDi);
                    localStorage.setItem('benDen', benDen);
                    localStorage.setItem('giaVe', chuyenxe[6])
                    // Correct usage of template literals inside the loop
                    var htmlContent = `
                    <div class="card mb-3" style="width: 30%;">
                        <div class="card-body">
                            <table class="table table-bordered table-striped table-sm">
                                <tbody>
                                    <tr><td><strong>Bến đi</strong></td><td>${chuyenxe[3]}</td></tr>
                                    <tr><td><strong>Bến đến</strong></td><td>${chuyenxe[4]}</td></tr>
                                    <tr><td><strong>Điểm đi</strong></td><td>${chuyenxe[1]}</td></tr>
                                    <tr><td><strong>Điểm đến</strong></td><td>${chuyenxe[2]}</td></tr>
                                    <tr><td><strong>Ngày đi</strong></td><td>${ngayDi}</td></tr>
                                    <tr><td><strong>Ngày về</strong></td><td>${ngayVe}</td></tr>
                                    <tr><td><strong>Chỗ ngồi đã chọn</strong></td><td>${choNgoi}</td></tr>
                                    <tr><td><strong>Khoảng cách</strong></td><td>${chuyenxe[5]} km</td></tr>
                                    <tr><td><strong>Giá vé</strong></td><td>${chuyenxe[6]} VND</td></tr>
                                </tbody>
                            </table>
                            <a href="/thanhtoan" class="btn btn-primary btn-sm">Đặt vé</a>
                        </div>
                    </div>
                    `;
                    resultContainer.innerHTML += htmlContent;
                });
            } else {
                console.log("Không tìm thấy chuyến xe.");
                var resultContainer = document.getElementById('resultContainer');
                resultContainer.innerHTML = '<p>Không tìm thấy chuyến xe với các thông tin đã nhập.</p>';
            }
        })
        .catch(error => {
            console.error("Lỗi khi gọi API:", error);
            var resultContainer = document.getElementById('resultContainer');
            resultContainer.innerHTML = '<p>Đã xảy ra lỗi khi truy xuất dữ liệu.</p>';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    let TTdiemDi = localStorage.getItem('diemDi');
    let TTdiemDen = localStorage.getItem('diemDen');
    let TTbenDi = localStorage.getItem('benDi');
    let TTbenDen = localStorage.getItem('benDen');
    let TTngayDi = localStorage.getItem('ngayDi');
    let TTngayVe = localStorage.getItem('ngayVe');
    let TTgiaVe = localStorage.getItem('giaVe');
    let TTchoNgoi = localStorage.getItem('choNgoi')

    TTdiemDi = TTdiemDi ? TTdiemDi : 'Chưa có thông tin';
    TTdiemDen = TTdiemDen ? TTdiemDen : 'Chưa có thông tin';
    TTbenDi = TTbenDi ? TTbenDi : 'Chưa có thông tin';
    TTbenDen = TTbenDen ? TTbenDen : 'Chưa có thông tin';
    TTngayDi = TTngayDi ? TTngayDi : 'Chưa có thông tin';
    TTngayVe = TTngayVe ? TTngayVe : 'Chưa có thông tin';
    TTgiaVe = TTgiaVe ? TTgiaVe : 'Chưa có thông tin';
    TTchoNgoi = TTchoNgoi ? TTchoNgoi : 'Chưa có thông tin';

    document.getElementById('diemdi').textContent = TTdiemDi;
    document.getElementById('diemden').textContent = TTdiemDen;
    document.getElementById('bendi').textContent = TTbenDi;
    document.getElementById('benden').textContent = TTbenDen;
    document.getElementById('ngaydi').textContent = TTngayDi;
    document.getElementById('ngayve').textContent = TTngayVe;
    document.getElementById('chongoi').textContent = TTchoNgoi;
    document.getElementById('giave').textContent = TTgiaVe + "VND";
});
