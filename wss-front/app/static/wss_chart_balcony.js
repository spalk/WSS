am4core.ready(function(){
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var div = chart_south_balcony
    var data_from_service = DataYandex
    var data_real = DataNarodmon

    //params
    var lighten = 0.7
    var transDur = 1000
    var transDurDiff = 300
    var tensX = 0.7

    var chart = am4core.create(div, am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.data = data_from_service;

    // console.log(chart.data)

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    //valueAxis.tooltip.disabled = true;

    // current datetime vertical line
    var range = dateAxis.axisRanges.create();
    range.date = new Date();
    range.grid.stroke = am4core.color("black");
    range.grid.strokeWidth = 2;
    range.grid.strokeOpacity = 1;

    // latest max
    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "latest_max";
    series2.tooltipText = "latest max: {valueY.value}";
    series2.sequencedInterpolation = true;
    series2.defaultState.transitionDuration = transDur;
    transDur += transDurDiff
    series2.tensionX = tensX;
    series2.stroke = am4core.color("red");
    series2.name = "forecast max"

    // latest min
    var series3 = chart.series.push(new am4charts.LineSeries());
    series3.dataFields.dateX = "date";
    series3.dataFields.valueY = "latest_min";
    series3.dataFields.openValueY = "latest_max";
    series3.fillOpacity = 0.1;
    series3.tooltipText = "latest min: {valueY.value}";
    series3.sequencedInterpolation = true;
    series3.defaultState.transitionDuration = transDur;
    transDur += transDurDiff
    series3.tensionX = tensX;
    series3.stroke = am4core.color("blue")
    series3.name = "forecast min"

    //sensor t curve
    var series4 = chart.series.push(new am4charts.LineSeries())
    series4.data = DataSensorT
    series4.dataFields.dateX = "date";
    series4.dataFields.valueY = "absolute_max";
    series4.stroke = am4core.color("red");
    series4.strokeWidth = 2;
    series4.tensionX = 0.9;
    series4.tooltipText = "fact: {valueY.value}";
    series4.defaultState.transitionDuration = transDur;
    series4.name = "inside"

    //narodmon curve
    var series5 = chart.series.push(new am4charts.LineSeries())
    series5.data = data_real
    series5.dataFields.dateX = "date";
    series5.dataFields.valueY = "absolute_max";
    series5.stroke = am4core.color("green");
    series5.strokeWidth = 1;
    series5.tensionX = 0.9;
    series5.tooltipText = "fact: {valueY.value}";
    series5.defaultState.transitionDuration = transDur;
    series5.name = "outside"

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.scrollbarX = new am4core.Scrollbar();

    // Create a horizontal scrollbar with previe and place it underneath the date axis
    chart.scrollbarX = new am4charts.XYChartScrollbar();
    chart.scrollbarX.series.push(series2);
    chart.scrollbarX.series.push(series3);
    chart.scrollbarX.parent = chart.bottomAxesContainer;

    // legend
    chart.legend = new am4charts.Legend();
    chart.legend.useDefaultMarker = true;
    var marker = chart.legend.markers.template.children.getIndex(0);
    marker.cornerRadius(12, 12, 12, 12);
    marker.strokeWidth = 2;
    marker.strokeOpacity = 1;
    marker.stroke = am4core.color("#ccc");

    dateAxis.start = 0.5;
    dateAxis.keepSelection = true;
    }
); // end am4core.ready()