var chart;
$(document).ready(function() {
   
   var colors = Highcharts.getOptions().colors,
      categories = ['MSIE', 'Firefox', 'Chrome', 'Safari', 'Opera'],
      name = 'Browser brands',
      level = 0,
      data = [{ 
            y: 55.11,
            color: colors[0],
            drilldown: {
               name: 'MSIE versions',
               categories: ['MSIE 8.0', 'MSIE 6.0', 'MSIE 7.0', 'MSIE 9.0'],
               level: 1, 
               data: [{
                   y: 33.06,
                   drilldown: {
                       level: 2,
                       name: 'drilldown next level',
                       categories: ['a', 'b', 'c'],
                       data: [23,54,47],
                       color: colors[0]
                   }
               }, 10.85, 7.35, 2.41],
               color: colors[0]
            }
         }, {
             y: 21.63,
            color: colors[1],
            drilldown: {
               name: 'Firefox versions',
               categories: ['Firefox 3.6', 'Firefox 4.0', 'Firefox 3.5', 'Firefox 3.0', 'Firefox 2.0'],
               data: [13.52, 5.43, 1.58, 0.83, 0.20],
               color: colors[1]
            }
         }, {
            y: 11.94,
            color: colors[2],
            drilldown: {
               name: 'Chrome versions',
               categories: ['Chrome 10.0', 'Chrome 11.0', 'Chrome 8.0', 'Chrome 9.0', 'Chrome 12.0', 
                  'Chrome 6.0', 'Chrome 5.0', 'Chrome 7.0'],
               data: [9.91, 0.50, 0.36, 0.32, 0.22, 0.19, 0.12, 0.12],
               color: colors[2]
            }
         }, {
            y: 7.15,
            color: colors[3],
            drilldown: {
               name: 'Safari versions',
               categories: ['Safari 5.0', 'Safari 4.0', 'Safari Win 5.0', 'Safari 4.1', 'Safari/Maxthon', 
                  'Safari 3.1', 'Safari 41'],
               data: [4.55, 1.42, 0.23, 0.21, 0.20, 0.19, 0.14],
               color: colors[3]
            }
         }, {
            y: 2.14,
            color: colors[4],
            drilldown: {
               name: 'Opera versions',
               categories: ['Opera 11.x', 'Opera 10.x', 'Opera 9.x'],
               data: [1.65, 0.37, 0.12],
               color: colors[4]
            }
         }];
   
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