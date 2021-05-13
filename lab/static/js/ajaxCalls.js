//
//


console.table(lendings);

fillActiveLendings();

function createLending() {
    let accountNumber = +document.querySelector('#accountNumber').value;
    let patrimonialNumber = document.querySelector('#patrimonialNumber').value;

    let accountExists = false;
    let patrimonialExists = false;

    /*Checking if those are valid values */
    for (let student of students) {
        if (student['accountNumber'] == accountNumber) {
            accountExists = true;
            break;
        }
    }

    for (let item of items) {
        if (item['patrimonialNumber'] == patrimonialNumber) {
            patrimonialExists = true;
            break;
        }
    }

    if (accountExists == false || patrimonialExists == false) {
        M.toast({ html: '❌ Equipo o usuario no existe', classes: 'rounded' });
        return -1;
    }
    /* Checking for duplicates*/

    for (let lending of lendings) {
        if (lending['accountNumber'] == accountNumber &&
            lending['patrimonialNumber'] == patrimonialNumber) {
            M.toast({ html: '⛔ Prestamo duplicado', classes: 'rounded' });
            return -1;
        }
    }

    /*Sending the ajax request*/

    $.ajax({
        url: 'createLending',
        data:
        {
            'accountNumber': accountNumber,
            'patrimonialNumber': patrimonialNumber,
        },
        success: function (newLendings) {
            M.toast({ html: '✅ Prestamo exitoso', classes: 'rounded' });
            lendings = newLendings;
            fillActiveLendings();
        },
    });
}

function generateReport() {
    initialRange = document.querySelector("#initialRange").value;
    endRange = document.querySelector("#endRange").value;
    careersSelected = document.querySelector("#careerSelect").value;
    console.log(initialRange, endRange, careersSelected);

    $.ajax(
        {
            url: 'generateReport',
            method:'POST',
            data: {
                'initialDate': initialRange,
                'endDate': endRange,
                'career': careersSelected
            },
            success: (pdf) => {
                alert("done");
            }
        }
    )
}

function returnLending(id) {
    $.ajax({
        url: 'returnLending',
        data:
        {
            'id': id,
        },
        success: function (data) {
            lendings = data['lendings']
            historialLendings = data['historialLendings'];
            fillActiveLendings();
            updatePieChart();
        },
    });
}

function returnAllLendings() {
    $.ajax({
        url: 'returnAllLendings',
        success: function (data) {
            lendings = data['lendings']
            historialLendings = data['historialLendings'];
            fillActiveLendings();
            updatePieChart();
        },
    });
}