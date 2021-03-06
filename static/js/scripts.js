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
      
      for(let i = 0; i < msg[4].length; i++ ){
        tabla += `<tr><td>${i+1}</td><td>${new Date(msg[5][i]).toLocaleDateString()}</td><td>${msg[4][i]}</td><td>${msg[2][i]}</td><td>${msg[3][i]}</td></tr>`; 
      }
      $('#tablat').show();
      $('#container').show();
      $('#container1').show();
      $('#tablat tbody tr').remove();
      $('#tablat').append(tabla);
      gr('container',datos,'Similitud Jaccard');
      gr('container1',datos1,'Similitud Coseno');
    },timeout : 300000,
    error :function(err){
      $('#loadingmessage').hide();
      $('#boton').attr("disabled", false);
      console.log(err);
      }
  })
}

function consulta(){
   $('#loadingmessage1').show();
   $('#boton1').attr("disabled", true);
  $.ajax({
    url:'/lit3',
    data:{tweet : $('#tweet').val()},
    type: 'POST',
    success: function(msg){
      $('#loadingmessage1').hide();
      $('#boton1').attr("disabled", false);
      $('#tw').text($('#tweet').val());
      $('#pol').text('Polaridad: '+msg[0]);
      $('#subj').text('Subjetividad: ' +msg[1]);
      $('#tweet').val('');
    },
    error :function(err){console.log(err);}
  })
}

function cargar(){
  $('#loadingmessage2').show();
  $.ajax({
    url:'/lit2',
    type: 'POST',
    success: function(msg){
      $('#loadingmessage2').hide();
      var tabla = `<tr><td>${msg[0]}</td><td>${msg[1]}</td></tr><tr><td>${msg[2]}</td><td>${msg[3]}</td></tr>`; 
      $('#mtc').html(tabla);
      $('#pp').text("Porcentaje de Positivos : "+(msg[0]/300).toFixed(2));
      $('#pn').text("Porcentaje de Negativos : "+(msg[3]/300).toFixed(2));
      $('#pe').text("Porcentaje de Error : "+((parseInt(msg[1])+parseInt(msg[2]))/300).toFixed(3));
      $('#pm').text("Precision del modelo : "+(msg[4]/1).toFixed(3));

      var twetsque = '<thead class="thead-dark"><th>#</th><th>Tweet</th><th>Etiquetado</th><th>Predicion</th></thead><tbody style="text-align:left">';
      for(let i = 0 ; i < msg[5].length; i++){
        var pole = '';
        var polp= '';
        if(msg[5][i] == 0){pole='Negativo'}else{pole='Positivo'}
        if(msg[6][i] == 0){polp='Negativo'}else{polp='Positivo'}

        twetsque+=`<tr><th scope="row">${i+1}</th><td>${msg[7][i]}</td><td>${pole}</td><td>${polp}</td></tr>`;
      }
      twetsque += '</tbody>';
     
      $('#tweque').html(twetsque);
    },
    error :function(err){console.log(err);}
  })
  
}

function calculartpm(){
   $('#loadingmessage4').show();
   $('#boton2').attr("disabled", true);
  $.ajax({
    url:'/topicm',
    data:{canttpm : $('#cantidadtpm').val()},
    type: 'POST',
    success: function(msg){
      $('#loadingmessage4').hide();
      $('#boton2').attr("disabled", false);

      let tabla = '';
      for(let i = 0; i < msg[0].length; i++ ){
        tabla += `<tr><td>${i+1}</td><td>${msg[0][i]}</td><td>${msg[2][i]}</td></tr>`; 
      }
      $('#stpm').show();
      $('#ttpm tbody tr').remove();
      $('#ttpm').append(tabla);
      $('#tpmp').text('Porcentaje de Positivos : '+msg[1][0]);
      $('#tpmn').text('Porcentaje de Negativos : ' +msg[1][1]);
      $('#tpmne').text('Porcentaje de Neutros : ' +msg[1][2]);
      $('#tpmt').text('Total de Topics : ' +msg[1][3]+' ');
      var imag = `<h3>Word Cloud</h3>`;
      imag += `<img src='/static/wordc/0.png' width="600px" heigth="550">`;
      $('#imgtp').html(imag);
    },timeout : 300000,
    error :function(err){
      $('#loadingmessage4').hide();
      $('#boton2').attr("disabled", false);
      console.log(err);
      }
  })
}