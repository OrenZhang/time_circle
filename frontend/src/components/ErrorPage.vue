<template>
    <div class="error-404" :style="{ 'background-image': imgUrl }">
    </div>
</template>


<script setup>
    import {computed} from "vue";

    const props = defineProps({
        img: {
            type: String,
            default: '/extra-assets/imgs/error404.png'
        }
    })

    const imgUrl = computed(() => 'url(' + props.img + ')')
</script>

<style scoped>
    .error-404 {
        box-sizing: border-box;
        padding: 20px;
        margin: 0 auto;
        max-width: 600px;
        width: 100%;
        height: 100%;
        background: white no-repeat center;
        background-size: contain;
    }
</style>