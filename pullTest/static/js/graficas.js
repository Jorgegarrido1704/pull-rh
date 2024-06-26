
    var ctx = document.getElementById('gaussChart').getContext('2d');

    // Parsear los datos JSON enviados desde la vista
    var data = JSON.parse('{{ data_json }}');
    var datosCalibre = data['{{ calibre }}'];

    console.log(data);

    console.log(datosCalibre);

    // Configuración del gráfico
