<template>
  <div class="video-player" :style="{ width: options.width, height: options.height }">
    <div data-vjs-player>
      <video ref="videoRef" class="video-js"></video>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';

export default {
  name: 'VideoPlayer',
  props: {
    options: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const videoRef = ref(null);
    let player = null;

    // 初始化 video.js 播放器
    const initPlayer = () => {
      if (videoRef.value) {
        player = videojs(videoRef.value, props.options);
      }
    };

    // 清理播放器资源
    const disposePlayer = () => {
      if (player) {
        player.dispose();
        player = null;
      }
    };

    onMounted(() => {
      initPlayer();
    });

    onUnmounted(() => {
      disposePlayer();
    });

    // 监听 options 属性的变化
    watch(() => props.options, (newOptions) => {
      // 如果需要根据 options 的变化来更新播放器配置，
      // 可以在这里重新初始化播放器等
      disposePlayer();
      initPlayer();
    }, {
      deep: true,
    });

    return {
      videoRef,
    };
  },
};
</script>

<style scoped>
/* 你可以在这里添加额外的样式 */
</style>
