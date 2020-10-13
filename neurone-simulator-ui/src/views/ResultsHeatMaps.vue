<template>
  <v-container>
    <v-toolbar></v-toolbar>
    <v-card heigth="100%" width="100%">
      <div ref="heatmap" style="width:100%; height: 400px;"></div>
    </v-card>
  </v-container>
</template>

<script>
import HeatmapJS from "heatmap.js/build/heatmap";
export default {
  data() {
    return {
      //selector data

      //heatmap data
      points: [],
      max: 0,
      width: 1150,
      height: 400,
      len: 200,
      heatmapInstance: {},
    };
  },
  methods: {
    setHeatMapData() {
      //console.log(this.$refs.heatmap);
      this.heatmapInstance = HeatmapJS.create({
        container: this.$refs.heatmap,
        maxOpacity: 0.5,
        radius: 30,
        blur: 0.8,
      });
      while (this.len--) {
        let val = Math.floor(Math.random() * 100);
        this.max = Math.max(this.max, val);
        const point = {
          x: 50,
          y: 50,
          value: 1000,
        };
        this.points.push(point);
      }
      // heatmap data format
      var data = {
        max: this.max,
        data: this.points,
      };
      // if you have a set of datapoints always use setData instead of addData
      // for data initialization
      //console.log(data);
      this.heatmapInstance.setData(data);
    },
  },
  mounted() {
    this.setHeatMapData();
  },
};
</script>

<style></style>
