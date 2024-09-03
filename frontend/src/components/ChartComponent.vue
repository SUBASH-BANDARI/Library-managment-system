<template>
  <Bar :data="chartData" />
</template>

<script>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);
import axios from "axios";

export default {
  name: "BarChart",
  components: { Bar },
  data() {
    return {
      //   chartData: {
      //     labels: [ 'January', 'February', 'March'],
      //     datasets: [
      //       {
      //         label: 'Data One',
      //         backgroundColor: '#f87979',
      //         data: [40, 20, 12]
      //       }
      //     ]
      //   }
    //   chartData: {
    //     labels: [],
    //     datasets: [
    //       {
    //         label: "Section Count",
    //         backgroundColor: "#f87979",
    //         data: [],
    //       },
    //     ],
    //   },
        chartData: null,
    };
  },
  methods: {
    async getData() {
      const response = await axios.get("http://localhost:5000/section_count", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      console.log(response.data);
      let section = response.data.sections;
      let section_names = [];
      let section_counts = [];
      for (let i = 0; i < section.length; i++) {
        section_names.push(section[i].title);
        section_counts.push(section[i].count);
      }
      this.chartData.data.labels = section_names;
      this.chartData.data.datasets[0].data = section_counts;
      this.chartData.update();
    },
  },
  async mounted() {
    await this.getData();
  },
};
</script>
