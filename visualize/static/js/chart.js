// var e = document.getElementById("ddlViewBy");
// var strUser = e.options[e.selectedIndex].value;
// var strUser = e.options[e.selectedIndex].text;


$(function myfunction() {     

    document.getElementById('btn').onclick=function(){         
        if(title.length < 2){              
            if(yname.length == 19){
                $('#container').highcharts({
                chart: {
                    type: 'line'
                },
                title: {
                    text: 'Subscriber Call Analysis'
                },
                xAxis: {
                    title: {
                    text:  category
                },
                    categories: xname
                },
                yAxis: {
                    title: {
                        text: measure
                    }
                },
                series: [{
                    name: title,
                    data: yname
                }]
                }); 
            }
            else{
                $('#container').highcharts({
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Subscriber Call Analysis'
                },
                xAxis: {
                    title: {
                    text:  category
                },
                    categories: xname
                },
                yAxis: {
                    title: {
                        text: measure
                    }
                },
                series: [{
                    name: title,
                    data: yname
                }]
                }); 
            }

        }
        else{            
            var colors = Highcharts.getOptions().colors,
            categories =  xname[0],             
            name = title[0]
            // var categoryS=category[0]
            // ymeasure = measure[0]
            
             var data = [];
                for (var i = 0; i < xname[0].length ; i++) {
                   data.push({
                      y: yname[0][i],
                      color: colors[i%10],
                      level: 0,
                      drilldown: {
                        // categoryS=category[1],
                         name: title[1],
                         categories: xname[1],                         
                         data: yname[i+1],                         
                         // ymeasure: measure[1],
                         level: 1,
                         color: colors[i%10]
                      }
                   });
                }
        
            function setChart(name, categories, data, color) {
                chart.xAxis[0].setCategories(categories, false);
                chart.series[0].remove(false);
                chart.addSeries({
                    name: name,
                    data: data,
                    color: color || 'white'
                }, false);
                chart.redraw();
            }

            var chart = $('#container').highcharts({
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Subscriber Call Analysis'
                },
                subtitle: {
                    text: 'Click the columns to view details. Click again to go back.'
                },
                xAxis: {                                                  
                    categories: categories
                },
                yAxis: {
                    title: {
                        text:measure[0]
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
                                        setChart(drilldown.name, drilldown.categories, drilldown.data, drilldown.color);                                        
                                    } else { // restore
                                        setChart(name, categories, data);                                        
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
                                return this.y +'';
                            }
                        }
                    }
                },
                tooltip: {
                    formatter: function() {
                        var point = this.point,
                            s = this.x +':<b>'+ this.y +' seconds call duration</b><br/>';
                        if (point.drilldown) {
                            s += 'Click to view '+ point.category +' ';
                        } else {
                            s += 'Click to return ';
                        }
                        return s;
                    }
                },
                series: [{
                    name: name,
                    data: data,
                    color: 'white'
                }],
                exporting: {
                    enabled: true
                }
            })
            .highcharts(); // return chart
        }            
    };        
});

