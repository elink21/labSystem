console.table(items);
updateAuditTable('');
updatePieChart();

clock = setInterval(function() {
    var d= new Date();
    let c=document.querySelector('#clockText');
    c.innerHTML= d.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
},100);

function updateAuditTable(toSearch) {

    toSearch = toSearch.toLowerCase();
    let newTableRows = "";
    let tableBody = document.querySelector('#tableBody');

    tableBody.innerHTML = '';
    for (let item of items) {
        if (item['patrimonialNumber'].includes(toSearch) ||
            item['name'].toLowerCase().includes(toSearch) ||
            item['brand'].toLowerCase().includes(toSearch) ||
            item['model'].toLowerCase().includes(toSearch)) {
            newTableRows += `
                    <tr>
                        <td>${item['patrimonialNumber']}</td>
                        <td>${item['name']}</td>
                        <td>${item['brand']}</td>
                        <td>${item['model']}</td>
                    </tr>
                `
        }
    }

    tableBody.innerHTML = newTableRows;
}

function clearFields() {
    let fields = [];
    fields.push(document.querySelector('#studentName'));
    fields.push(document.querySelector('#career'));
    fields.push(document.querySelector('#itemName'));
    fields.push(document.querySelector('#brand'));
    fields.push(document.querySelector('#model'));
    fields.push(document.querySelector('#accountNumber'));
    fields.push(document.querySelector('#patrimonialNumber'));

    for (let field of fields) {
        field.value = '';
    }


}

function autofillStudent(accountNumber) {
    let choosenOne = null;
    let nameInput = document.querySelector('#studentName');
    let careerInput = document.querySelector('#career');


    for (let student of students) {
        if (student['accountNumber'] === +accountNumber) {
            choosenOne = student;
        }
    }

    if (choosenOne != null) {
        nameInput.value = choosenOne['name'];
        careerInput.value = choosenOne['career'];
    }
    else {
        nameInput.value = '';
        careerInput.value = '';
    }
}

function autofillItem(patrimonialNumber) {
    let choosenOne = null;
    let nameInput = document.querySelector('#itemName');
    let brandInput = document.querySelector('#brand');
    let modelInput = document.querySelector('#model');

    for (let item of items) {
        if (item['patrimonialNumber'] === patrimonialNumber) {
            choosenOne = item;
        }
    }

    if (choosenOne != null) {


        nameInput.value = choosenOne['name'];
        brandInput.value = choosenOne['brand'];
        modelInput.value = choosenOne['model'];
    }
    else {
        nameInput.value = '';
        brandInput.value = '';
        modelInput.value = '';
    }
}

function updatePieChart() {
    var ctx = document.querySelector('#chart').getContext('2d');
    data = {
        datasets: [{
            data: [10, 20, 30]
        }],
    
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Red',
            'Yellow',
            'Blue'
        ]
    };

    var myDoughnutChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: {
            title: {
                display: true,
                text: 'Usuarios por carrera',
                fontSize:12,
                fontStyle:'bold',
            }
        }
    });
}