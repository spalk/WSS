am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("chart_yandex2", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.data = DataYandex2;

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;

    // current datetime vertical line
    var range = dateAxis.axisRanges.create();
    range.date = new Date();
    range.grid.stroke = am4core.color("red");
    range.grid.strokeWidth = 2;
    range.grid.strokeOpacity = 1;

    // absolute max
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    //series.dataFields.openValueY = "open";
    series.dataFields.valueY = "absolute_max";
    //series.tooltipText = "min: {openValueY.value} max   : {valueY.value}";
    series.sequencedInterpolation = true;
    //series.fillOpacity = 0.1;
    series.defaultState.transitionDuration = 1000;
    series.tensionX = 0.8;
    series.stroke = am4core.color("green");

    // latest max
    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "latest_max";
    series2.sequencedInterpolation = true;
    series2.defaultState.transitionDuration = 1500;
    //series2.stroke = chart.colors.getIndex(6);
    series2.tensionX = 0.8;
    series2.stroke = am4core.color("blue");

    // latest min
    var series3 = chart.series.push(new am4charts.LineSeries());
    series3.dataFields.dateX = "date";
    series3.dataFields.valueY = "latest_min";
    series3.sequencedInterpolation = true;
    series3.defaultState.transitionDuration = 2000;
    //series3.stroke = chart.colors.getIndex(6);
    series3.tensionX = 0.8;
    series3.stroke = am4core.color("pink");

    // absolute min
    var series4 = chart.series.push(new am4charts.LineSeries());
    series4.dataFields.dateX = "date";
    series4.dataFields.valueY = "absolute_min";
    series4.sequencedInterpolation = true;
    series4.defaultState.transitionDuration = 2500;
    //series4.stroke = chart.colors.getIndex(6);
    series4.tensionX = 0.8;
    series4.stroke = am4core.color("orange");

    //narodmon curve
//    var series3 = chart.series.push(new am4charts.LineSeries())
//    series3.data = DataNarodmon
//    series3.dataFields.dateX = "date";
//    series3.dataFields.valueY = "open";
//    series3.stroke = am4core.color("green");
//    series3.strokeWidth = 3;
//    series3.fillOpacity = 0.1;
//    series3.tooltipText = "val: {valueY.value}";

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.scrollbarX = new am4core.Scrollbar();

}); // end am4core.ready()
