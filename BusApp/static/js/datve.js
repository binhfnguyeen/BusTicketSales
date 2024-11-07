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

            diemDiSelect.addEventListener('change', function() {
                console.log("Điểm đi: " + diemDiSelect.value);
            });
            diemDenSelect.addEventListener('change', function() {
                console.log("Điểm đến: " + diemDenSelect.value);
            });
            quanHuyenDiSelect.addEventListener('change', function() {
                console.log("Quận huyện đi: " + quanHuyenDiSelect.value);
            });
            quanHuyenDenSelect.addEventListener('change', function() {
                console.log("Quận huyện đến: " + quanHuyenDenSelect.value);
            });
            benDiSelect.addEventListener('change', function(){
                console.log("Bến đi: "+benDiSelect.value)
            })
            benDenSelect.addEventListener('change', function(){
                console.log("Bến đến: "+benDenSelect.value)
            })
        })
        .catch(error => console.error('Error fetching data:', error));
};

function showResult() {
    document.querySelector('.bresult').style.display = 'block';
    const diemDi = document.querySelector('#diem_di').value;
    const diemDen = document.querySelector('#diem_den').value;
    const ngayDi = document.getElementById('ngay_di').value;
    const ngayVe = document.getElementById('ngay_ve').value;

    if (diemDi && diemDen && ngayDi && ngayVe) {
        const resultHtml = `
            <div class="card mb-3" style="width: 30%;">
                <div class="card-body">
                    <div class="container-sm">
                        <table class="table table-bordered table-striped table-sm">
                            <tbody>
                                <tr><td><strong>Điểm đi</strong></td><td><span>${diemDi}</span></td></tr>
                                <tr><td><strong>Điểm đến</strong></td><td><span>${diemDen}</span></td></tr>
                                <tr><td><strong>Ngày đi</strong></td><td><span>${ngayDi}</span></td></tr>
                                <tr><td><strong>Ngày về</strong></td><td><span>${ngayVe}</span></td></tr>
                            </tbody>
                        </table>
                        <button class="btn btn-danger mt-3 btn-sm">Đặt vé</button>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('resultContainer').innerHTML = resultHtml;
    } else {
        alert("Vui lòng chọn đủ các trường!");
    }
}
