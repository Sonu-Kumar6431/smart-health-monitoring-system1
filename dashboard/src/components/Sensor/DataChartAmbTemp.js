import React, { useEffect, useRef } from "react";
import { Line } from "react-chartjs-2";
import StreamingPlugin from "chartjs-plugin-streaming";
import "chartjs-adapter-date-fns";

import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  TimeScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  LinearScale,
  PointElement,
  LineElement,
  TimeScale,
  Tooltip,
  Legend,
  StreamingPlugin
);

const ChartComponent = ({ timestamp, sensorValue }) => {
  const savedData = useRef({ timestamp: null, sensorValue: null });

  useEffect(() => {
    savedData.current = { timestamp, sensorValue };
  }, [timestamp, sensorValue]);

  const onRefresh = (chart) => {
    const { timestamp, sensorValue } = savedData.current;

    if (!timestamp || sensorValue === null) return;

    chart.data.datasets[0].data.push({
      x: timestamp,
      y: sensorValue,
    });
  };

  return (
    <Line
      data={{
        datasets: [
          {
            label: "Sensor Data",
            data: [],
            borderColor: "red",
            backgroundColor: "rgba(255,0,0,0.2)",
          },
        ],
      }}
      options={{
        animation: false,
        responsive: true,
        scales: {
          x: {
            type: "realtime",
            realtime: {
              duration: 30000,
              refresh: 1000,
              delay: 2000,
              onRefresh: onRefresh,
            },
          },
          y: {
            beginAtZero: true,
          },
        },
      }}
    />
  );
};

export default ChartComponent;