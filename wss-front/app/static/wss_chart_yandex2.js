am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    //params
    var lighten = 0.7
    var transDur = 1000
    var transDurDiff = 300

    var chart = am4core.create("chart_yandex2", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.data = DataYandex2;

    console.log(DataYandex2)

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
    series.tooltipText = "absolute max: {valueY.value}";
    series.sequencedInterpolation = true;
    //series.fillOpacity = 0.1;
    series.defaultState.transitionDuration = transDur;
    transDur += transDurDiff
    series.tensionX = 0.8;
    series.stroke = am4core.color("red").lighten(+lighten);;

    // latest max
    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "latest_max";
    series2.tooltipText = "latest max: {valueY.value}";
    series2.sequencedInterpolation = true;
    series2.defaultState.transitionDuration = transDur;
    transDur += transDurDiff
    series2.tensionX = 0.8;
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
    series3.tensionX = 0.8;
    series3.stroke = am4core.color("blue")

    // absolute min
    var series4 = chart.series.push(new am4charts.LineSeries());
    series4.dataFields.dateX = "date";
    series4.dataFields.valueY = "absolute_min";
    series4.tooltipText = "absolute min: {valueY.value}";
    series4.sequencedInterpolation = true;
    series4.defaultState.transitionDuration = transDur;
    transDur += transDurDiff
    series4.tensionX = 0.8;
    series4.stroke = am4core.color("blue").lighten(+lighten);;

    //narodmon curve
    /*var series3 = chart.series.push(new am4charts.LineSeries())
    series3.data = DataNarodmon
    series3.dataFields.dateX = "date";
    series3.dataFields.valueY = "open";
    series3.stroke = am4core.color("green");
    series3.strokeWidth = 3;
    series3.fillOpacity = 0.1;
    series3.tooltipText = "val: {valueY.value}";*/

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.scrollbarX = new am4core.Scrollbar();

}); // end am4core.ready()
