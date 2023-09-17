import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

const PlotComponent = () => {
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

  // Generate random data for 100 lines
  const numberOfLines = 10;
  const dataArray = [];
  for (let i = 0; i < numberOfLines; i++) {
    const lineData = [];
    for (let j = 0; j < 10; j++) {
      lineData.push(Math.random() * 10); // Generate random data
    }
    dataArray.push(lineData);
  }

  const labels = Array(10)
    .fill(0)
    .map((_, i) => i.toString()); // Labels as an array of strings

  // Create an array of datasets, one for each line
  const datasets = dataArray.map((data, index) => ({
    label: `Line ${index + 1}`,
    data: data,
    borderColor: getRandomColor(), // Generate a random color for each line
    backgroundColor: "rgba(0, 0, 0, 0)",
    pointBackgroundColor: getRandomColor(),
    pointBorderColor: getRandomColor(),
    pointRadius: 4,
    pointHoverRadius: 5,
    fill: false,
  }));

  // Function to generate a random color
  function getRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  const data = {
    labels: labels,
    datasets: datasets,
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        type: "linear",
        title: {
          display: true,
          text: "Index (X-Axis)",
          color: "white",
        },
        ticks: {
          color: "white",
        },
      },
      y: {
        title: {
          display: true,
          text: "Value (Y-Axis)",
          color: "white",
        },
        ticks: {
          color: "white",
        },
      },
    },
    plugins: {
      legend: {
        display: numberOfLines <= 10,
        labels: {
          display: numberOfLines <= 10,
          color: "white",
        },
      },
    },
  };

  return (
    <div style={{ height: "400px" }}>
      <Line data={data} options={options} />
    </div>
  );
};

export default PlotComponent;
