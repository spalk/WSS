function wssChart(div, data_from_service, data_real) {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

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

    // absolute max
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "absolute_max";
    series.tooltipText = "absolute max: {valueY.value}";
    series.sequencedInterpolation = true;
    series.defaultState.transitionDuration = transDur;
    transDur += transDurDiff
    series.tensionX = tensX;
    series.stroke = am4core.color("red").lighten(+lighten);;

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

    // absolute min
    var series4 = chart.series.push(new am4charts.LineSeries());
    series4.dataFields.dateX = "date";
    series4.dataFields.valueY = "absolute_min";
    series4.tooltipText = "absolute min: {valueY.value}";
    series4.sequencedInterpolation = true;
    series4.defaultState.transitionDuration = transDur;
    transDur += transDurDiff
    series4.tensionX = tensX;
    series4.stroke = am4core.color("blue").lighten(+lighten);;

    //narodmon curve
    var series5 = chart.series.push(new am4charts.LineSeries())
    series5.data = data_real
    series5.dataFields.dateX = "date";
    series5.dataFields.valueY = "absolute_max";
    series5.stroke = am4core.color("green");
    series5.strokeWidth = 2;
    series5.tensionX = 0.9;
    series5.tooltipText = "fact: {valueY.value}";
    series5.defaultState.transitionDuration = transDur;

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.scrollbarX = new am4core.Scrollbar();

    // Create a horizontal scrollbar with previe and place it underneath the date axis
    chart.scrollbarX = new am4charts.XYChartScrollbar();
    chart.scrollbarX.series.push(series2);
    chart.scrollbarX.series.push(series3);
    chart.scrollbarX.parent = chart.bottomAxesContainer;

    dateAxis.start = 0.5;
    dateAxis.keepSelection = true;
}

am4core.ready(function(){
    wssChart("chart_yandex", DataYandex, DataNarodmon);
    wssChart("chart_rp5", DataRP5, DataNarodmon);
}); // end am4core.ready()