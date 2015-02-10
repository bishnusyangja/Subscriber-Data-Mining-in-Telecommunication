var chart;
var colors = Highcharts.getOptions().colors;     

function getData(var i)
{
  var datax=[];
  for (var j = 0; j < xname[1].length ; j++) {
    datax.push({
      y: yname[i+1][j],
        color: colors[0],
        drilldown: {
           name: title[2],
           categories: xname[2],
           level: 2,                    
           data: yname[xname[0].length+xname[1].length*i+j+1],                         
           color: colors[0]
        }
      });                    
  }
  return datax;
}

$(document).ready(function() { 
      categories = xname[0],
      name = title[0],
      level = 0     
      var datam=[];
      for (var i = 0; i < xname[0].length ; i++) {
            datam.push({
              y: yname[0][i],
                color: colors[0],
                drilldown: {
                   name: title[1],
                   categories: xname[1],
                   level: 1,      
                   data:getData(i),
                   color:colors[0]
          }
        });                    
      }             
      data=datam;                  
   
   function setChart(name, categories, data, color, level) {
      chart.xAxis[0].setCategories(categories);
      chart.series[0].remove();
       
       
      chart.addSeries({
         name: name,
         data: data,
         level: level,
         color: color || 'white'
      });
   }
   
   chart = new Highcharts.Chart({
      chart: {
         renderTo: 'container', 
         type: 'column'
      },
      title: {
         text: 'Browser market share, April, 2011'
      },
      subtitle: {
         text: 'Click the columns to view versions. Click again to view brands.'
      },
      xAxis: {
         categories: categories                     
      },
      yAxis: {
         title: {
            text: 'Total percent market share'
         }
      },
      plotOptions: {
         column: {
            cursor: 'pointer',
            point: {
               events: {
                  click: function() {

                     var drilldown = this.drilldown;
                     if (drilldown) { // drill down
                         
                         this.series.chart.setTitle({
                             text: drilldown.name
                         });
                     
                         setChart(drilldown.name, drilldown.categories, drilldown.data, drilldown.color, drilldown.level);
                     } else { // restore
                        setChart(name, categories, data, null, level);
                     }
                  }
               }
            },
            dataLabels: {
               enabled: true,
               color: colors[0],
               style: {
                  fontWeight: 'bold'
               },
               formatter: function() {
                  return this.y +'%';
               }
            }               
         }
      },
      tooltip: {
         formatter: function() {
            var point = this.point, s = '';
            
             switch (this.series.options.level) {
                case 0:
                    s = 'LEVEL ONE<br/>';
                    s += ' INSTRUCTIONS HERE 111';
                    break;
                
                case 1:
                    s = 'LEVEL TWO INSTRUCTIONS HERE <br/>';
                    s += ' INSTRUCTIONS HERE 222';
                    break;
                
                case 2:
                    s = 'LEVEL THREE INSTRUCTIONS HERE<br/>';
                    s += 'INSTRUCTIONS HERE 333';
                    break;
             }
             
             
            return s;
         }
      },
      series: [{
         name: name,
         level: level,
         data: data,
         color: 'white'
      }],
      exporting: {
         enabled: false
      }
   });
   
   
});












