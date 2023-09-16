import Plot from "react-plotly.js";

const PlotComponent = () => {
  return (
    <Plot
      data={[
        {
          x: ["Jan", "Feb", "Mar", "Apr", "May"],
          y: [10, 15, 20, 18, 25],
          mode: "lines+markers",
          line: {
            color: "red", // Set the line color to red
            width: 2, // Set the line width
            // Set the line edge color to black
            // Use rgba to control the alpha (transparency) value
            // Here, we set it to fully opaque (255) for a solid edge
            // You can adjust the alpha value as needed
            shape: "linear",
            dash: "solid",
            linecolor: "rgba(121, 0, 0, 255)", // Set the line edge color to black
          },
          marker: {
            color: "rgba(222,55,61,1)",
            line: {
              width: 2.5,
              color: "rgba(0,0,0,1)",
            },
          },
        },
        // Add more traces for additional lines as needed
      ]}
      layout={{
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: {
          title: "Month",
          titlefont: {
            color: "white",
          },
          tickfont: {
            color: "white",
          },
        },
        yaxis: {
          title: "Value",
          titlefont: {
            color: "white",
          },
          tickfont: {
            color: "white",
          },
        },
        legend: {
          font: {
            color: "white",
          },
        },
      }}
    />
  );
};

export default PlotComponent;
