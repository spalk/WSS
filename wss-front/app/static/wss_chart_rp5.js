am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("chart_rp5", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.data = DataRP5;

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;

    // current date vertical line
    var range = dateAxis.axisRanges.create();
    range.date = new Date();
    range.grid.stroke = am4core.color("red");
    range.grid.strokeWidth = 2;
    range.grid.strokeOpacity = 1;

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.openValueY = "open";
    series.dataFields.valueY = "close";
    series.tooltipText = "min: {openValueY.value} max   : {valueY.value}";
    series.sequencedInterpolation = true;
    series.fillOpacity = 0.1;
    series.defaultState.transitionDuration = 1000;
    series.tensionX = 0.8;

    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "open";
    series2.sequencedInterpolation = true;
    series2.defaultState.transitionDuration = 1500;
    series2.stroke = chart.colors.getIndex(6);
    series2.tensionX = 0.8;

    //narodmon curve
    var series3 = chart.series.push(new am4charts.LineSeries())
    series3.data = DataNarodmon
    series3.dataFields.dateX = "date";
    series3.dataFields.valueY = "open";
    series3.stroke = am4core.color("green");
    series3.strokeWidth = 3;

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.scrollbarX = new am4core.Scrollbar();

}); // end am4core.ready()
