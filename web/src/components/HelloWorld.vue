<template>
  <div class="video-list">
    <div v-for="video in videoList" :key="video" class="video-item">
      <h3>{{ video }}</h3>
      <VideoPlayer :options="{
      autoplay: false,
      controls: true,
      responsive: true,
      fluid: true,
      playbackRates: [0.5, 1, 1.5, 2, 3],
      width: '900px',
      height: '100%',
      sources: [{
        src: `${BASE_URL}/video?video_name=${video}`,
        type: 'video/mp4'
      }]
    }" />
    </div>
  </div>


</template>

<script setup>
import { ref, onMounted } from 'vue'
import VideoPlayer from './VideoPlayer.vue'
import { getVideos } from '@/api/video'
const videoList = ref([]);
const BASE_URL = import.meta.env.VITE_API_BASE_URL
const play = () => {

}

onMounted(() => {
  getVideos().then(req => {
    videoList.value = req
  });

});


</script>


<style scoped></style>
