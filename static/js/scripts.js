function gr (contenedor,series,nombre){
      var myChart = Highcharts.chart(contenedor, {
            chart: {
                type: 'pie'
            },
            title: {
                text: nombre
            },
            xAxis: {
                categories: ['Positivos', 'Negativos', 'Neutros']
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            plotOptions: {
            pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                connectorColor: 'silver'
            }
        }
    },
            series: [{
              name: nombre,
              data: series
            }]
        });
}
function graficar(){
   $('#loadingmessage').show();
   $('#boton').attr("disabled", true);
  $.ajax({
    url:'/lit1',
    data:{cant : $('#cantidad').val()},
    type: 'POST',
    success: function(msg){
      $('#loadingmessage').hide();
      $('#boton').attr("disabled", false);
      $('#jp').text(msg[0][0]+'%');
      $('#jn').text(msg[0][1]+'%');
      $('#jne').text(msg[0][2]+'%');
      $('#jt').text(msg[0][3]);
      $('#cp').text(msg[1][0]+'%');
      $('#cn').text(msg[1][1]+'%');
      $('#cne').text(msg[1][2]+'%');
      $('#ct').text(msg[1][3]);
      let datos = [
        {name: 'positivos',y:msg[0][0]},
        {name: 'Negativos',y:msg[0][1]},
        {name: 'Neutros',y:msg[0][2]} 
      ];
      let datos1 = [
        {name: 'positivos',y:msg[1][0]},
        {name: 'Negativos',y:msg[1][1]},
        {name: 'Neutros',y:msg[1][2]} 
      ];
      let tabla = ''
      for(let i = 0; i < msg[2].length; i++ ){
        tabla += `<tr><td>${i+1}</td><td>${msg[2][i]}</td></tr>`; 
      }
      $('#tablat tbody tr').not(':first').remove();
      $('#tablat').append(tabla);
      gr('container',datos,'Similitud Jaccard');
      gr('container1',datos1,'Similitud Coseno');
    },
    error :function(err){console.log(err)}
  })
}