/*Global variables */

let chart;
let careers=['Ingenieria en computacion','Informatica administrativa'];
let chartData=[300,121];

console.table(historialLendings);

/*Initializing functions */
updateAuditTable('');
initPieChart();
fillActiveLendings();

updatePieChart();



clock = setInterval(function () {
    var d = new Date();
    let c = document.querySelector('#clockText');
    c.innerHTML = d.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
}, 100);

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

function initPieChart() {

    ctx = document.querySelector('#chart').getContext('2d');
    data = {
        datasets: [{
            data: chartData,
            backgroundColor: [
                'rgba(44, 82, 52, 1)',
                'rgba(156, 132, 18, 1)',
                'rgba(0, 128, 0,1)',
                'rgba(179, 149, 60,1)',
            ],
        }],
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: careers,
    };

    chart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            title: {
                display: true,
                text: 'Usuarios por carrera',
                fontSize: 12,
                fontStyle: 'bold',
            }
        }
    });
}

function updatePieChart() {
    let data={};
    let labels=[];
    let registers=[];
    for(let lending of historialLendings)
    {
        let career= searchByField(students,'accountNumber', lending['accountNumber'])[0]['career']; 
        data.hasOwnProperty(career)? data[career]+=1: data[career]=1;
    }


    for(key in data)
    {
        labels.push(key);
        registers.push(data[key]);
    }

    chart.data.labels=labels;
    chart.data.datasets[0]['data']=registers;
    chart.update();
    console.log(labels,registers);
}

function searchByField(list, field, value) {
    let matches = [];
    for (element of list) {
        if (element[field] == value) {
            matches.push(element);
        }
    }
    return matches;
}

function fillActiveLendings() {
    let container = document.querySelector('#lendingsContainer');
    let accountNumber = +document.querySelector('#accountNumberReturn').value;
    container.innerHTML = '';
    let html = '';

    for (lending of lendings) {
        let studentName = searchByField(students, 'accountNumber', lending['accountNumber'])[0]['name'];
        let studentAccount = searchByField(students, 'accountNumber', lending['accountNumber'])[0]['accountNumber'];
        let itemName = searchByField(items, 'patrimonialNumber', lending['patrimonialNumber'])[0]['name'];
        let card = `
        <div class="lendingCard z-depth-2">
          <div>
            <i class="material-icons rounded">person</i> <br />
            <small>${studentName}</small>
          </div>
          <br />
          <div>
            <i class="material-icons rounded">memory</i> <br />
            <small>${itemName}</small>
          </div>

          <a onclick="returnLending(${lending['id']})" class="waves-effect waves-light btn-small green darken-4">
            Devolver
          </a>
        </div>
        `;

        /* Filtering by account number */
        if (accountNumber == '' || studentAccount == accountNumber) {
            html += card;
        }

    }
    container.innerHTML = html;
}