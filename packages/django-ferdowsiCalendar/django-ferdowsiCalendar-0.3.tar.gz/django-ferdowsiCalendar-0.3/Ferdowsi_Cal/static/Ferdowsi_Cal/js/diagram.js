google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawRightY);


function scale(array){
    let output=array
    myMax = parseInt(output[0][1])

    for(i=0; i< output.length; i++){
        if(myMax<parseInt(output[i][1])){
            myMax = parseInt(output[i][1])
        }
    }
    for(i=0; i< output.length; i++){
        array[i][1] = (output[i][1]*5/myMax)
    }
    return output;
}

function drawRightY() {

var dataTable = new google.visualization.DataTable();
        dataTable.addColumn('string', 'User');
        dataTable.addColumn('number', 'Events');
        dataTable.addColumn('number', 'Salary');
        let m = scale(myUsers_Fields)
        for(i=0; i<myUsers_Fields.length; i++){
            dataTable.addRows([[m[i][0],parseInt([myUsers_Fields[i][2]]), {v:parseInt(m[i][1]),f:Math.round(myUsers_Fields[i][1]*myMax/5)+'$'}]])
    }

       var materialOptions = {
        chart: {
          title: "Impact of Events on "+myCol,
          subtitle: 'For each user'
        },

        axes: {
            y: {
                all: {
                    range: {
                        max: 5,
                        min: 0
                    }
                }
            }
        },
        colors: ['blue','green'],
        bars: 'vertical', // Required for Material Bar Charts.
        width: 800,
        height: 600
    };
      var materialChart = new google.charts.Bar(document.getElementById('chart_div'));
      materialChart.draw(dataTable, materialOptions);
    }
