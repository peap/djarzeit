$(document).ready(function(){

    // Setup SVG container
    var nRows = window.timelineData.nCategories;
    var height = 150 + 50 * nRows;
    var width = $('#timeline').width();
    var margin = {
        'top': 15,
        'bottom': 25,
        'left': 0.05 * width,
        'right': 0.05 * width,
    }
    var h = height - margin.top - margin.bottom;
    var w = width - margin.right - margin.left;

    var svg = d3.select('#timeline')
        .append('svg')
        .attr('height', height)
        .attr('width', width);

    // Add title
    var title = svg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .attr('class', 'title')
      .append('text')
       .attr('x', (w / 2))
       .attr('y', margin.top)
       .attr('text-anchor', 'middle')
       .text('Timeline of Intervals on ' + window.timelineData.dateStr);

    // Add axis
    var timeScale = d3.time.scale()
        .domain([window.timelineData.minHour, window.timelineData.maxHour])
        .range([0, w]);

    var timeAxis = d3.svg.axis()
        .scale(timeScale)
        .tickFormat(d3.time.format('%I:%M %p'))
        .orient('bottom');

    svg.append('g')
        .attr('class', 'time-axis')
        .attr('transform',
              'translate(' + margin.left + ',' + (height - margin.bottom - 50) + ')')
        .call(timeAxis)
      .selectAll('text')
        .attr('x', 9)
        .attr('y', 0)
        .attr('dy', '.35em')
        .attr('transform', 'rotate(90)')
        .style('text-anchor', 'start');

    // Add data
    function intervalX(d) { return margin.left + timeScale(d.start); }
    function intervalY(d) { return margin.top + d.categoryNum * 50; }
    function intervalGroupTransform(d) {
        return 'translate(' + intervalX(d) + ',' + intervalY(d) + ')';
    }
    function intervalClass(d) { return 'interval-of-category-' + d.categoryNum; }
    function intervalWidth(d) { return timeScale(d.end) - timeScale(d.start); }
    function intervalHeight(d) { return 35; }
    function intervalText(d) { return d.timerName; }
    function intervalTextX(d) { return 5; }
    function intervalTextY(d) { return intervalHeight(d) - 5; }

    // Create interval groups
    var intervals = window.timelineData.intervals;
    var intervalGroups = svg.selectAll('g.interval')
        .data(intervals)
        .enter()
      .append('g')
        .attr('class', 'interval')
        .attr('transform', intervalGroupTransform);

    // add rectangles to groups
    intervalGroups.append('rect')
        .attr('class', intervalClass)
        .attr('width', intervalWidth)
        .attr('height', intervalHeight);

    // add labels to groups
    intervalGroups.append('text')
        .text(intervalText)
        .attr('x', intervalTextX)
        .attr('y', intervalTextY)
        .style('text-anchor', 'start');

    // TODO: add category group labels on left-hand side

    // TODO: add hover handlers for showing more interval info

    // TODO: add click handlers for creating/editing/deleting intervals

});
