document.getElementById("sidebarMenu").style.paddingTop ="90px";

console.log("in dashboard");

if (window.innerWidth>1430) {
  document.getElementById("sidebarMenu").style.width = "280px"
  console.log("changed")
}
else if (window.innerWidth<1430 && window.innerWidth>1300) {
  document.getElementById("sidebarMenu").style.width = "240px"
  console.log("changed")
}
else if (window.innerWidth<1100 && window.innerWidth>990) {
  document.getElementById("sidebarMenu").style.width = "200px"
  console.log("changed")
}
else if (window.innerWidth<990 && window.innerWidth>767) {
  document.getElementById("sidebarMenu").style.width = "220px"
  console.log("changed")
}
else if (window.innerWidth<1300 && window.innerWidth>1100) {
  document.getElementById("sidebarMenu").style.width = "220px"
  console.log("changed")
}
else{
  console.log("else exicuted for sidebar")
}


if (window.innerWidth>665) {
  document.getElementById("navv").style.paddingRight = "90px"
}
else{
  console.log("else exicuted for navv")
}

if (window.innerWidth<620) {
  document.getElementById("myChart").style.height = "900";
  console.log("Chart hight 900")
}
else{
  console.log("else exicuted for mychart")
}







const getRandomType = () => {
  const types = [
    "bar",
    "horizontalBar",
    "pie",
    "line",
    "radar",
    "doughnut",
    "polarArea",
  ];
  return types[Math.floor(Math.random() * types.length)];
};


const renderChart = (data, labels) => {
  const type = getRandomType();
  var ctx = document.getElementById("myChart").getContext("2d");
  var myChart = new Chart(ctx, {
    type: type,
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months Complaint",
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Complaints per category",
      },
    },
  });
};

const getChartData = () => {
  console.log("fetching");
  fetch("/Complaints/complaint_category_summary")
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const category_data = results.complaint_category_data;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];

      renderChart(data, labels);
    });
};

document.onload = getChartData();
